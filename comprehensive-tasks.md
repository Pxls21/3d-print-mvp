# 📋 Development Tasks - Complete Checklist

## Overview

This document contains ALL implementation tasks for the 3D Print MVP project. Tasks are organized by phase and include:
- **Description**: What needs to be done
- **Archon Research**: What to look up using Archon MCP
- **Expected Output**: What you should have when complete
- **Estimated Time**: How long it should take
- **Dependencies**: What must be done first

---

## Task Index

### Phase 1: Foundation & Local Development (Weeks 1-2)
- [TASK_001](#task_001): Setup Development Environment
- [TASK_002](#task_002): TRELLIS Integration Test
- [TASK_003](#task_003): FreeCAD STL Validation
- [TASK_004](#task_004): Medusa.js Installation
- [TASK_005](#task_005): Custom 3D Processing Module
- [TASK_006](#task_006): Product Configuration

### Phase 2: GPU Processing Service (Weeks 3-4)
- [TASK_007](#task_007): Docker Image Creation
- [TASK_008](#task_008): RunPod Handler Implementation
- [TASK_009](#task_009): FastAPI Job Orchestrator
- [TASK_010](#task_010): Zero-Trust Security

### Phase 3: Frontend Development (Weeks 5-6)
- [TASK_011](#task_011): Next.js Storefront Setup
- [TASK_012](#task_012): Custom Upload Component
- [TASK_013](#task_013): Real-time Job Status
- [TASK_014](#task_014): Custom Admin Widgets
- [TASK_015](#task_015): System Monitoring

### Phase 4: Testing & Optimization (Weeks 7-8)
- [TASK_016](#task_016): Automated Testing Suite
- [TASK_017](#task_017): Performance Benchmarking
- [TASK_018](#task_018): Security Audit
- [TASK_019](#task_019): Production Deployment

### Phase 5: Launch & Monitoring (Week 9+)
- [TASK_020](#task_020): Beta User Testing
- [TASK_021](#task_021): Public Launch

---

## Phase 1 Tasks

### TASK_001: Setup Development Environment
**Phase**: 1 | **Week**: 1 | **Days**: 1-2 | **Time**: 8 hours

#### Description
Install and configure TRELLIS on your RTX 3090 system. Verify GPU access and test basic functionality.

#### Steps
1. Install CUDA 11.8 and cuDNN
2. Clone TRELLIS repository with submodules
3. Install Python dependencies
4. Test model loading
5. Benchmark processing time and VRAM usage

#### Archon Research Queries
```bash
archon query "TRELLIS installation guide for CUDA 11.8"
archon query "TRELLIS VRAM optimization techniques"
archon query "TRELLIS single image to 3D API"
archon query "Python environment setup for ML projects"
```

#### Implementation
```bash
# System setup
sudo dnf install cuda-11-8 python3.10-devel git

# Clone TRELLIS
git clone --recurse-submodules https://github.com/microsoft/TRELLIS.git
cd TRELLIS

# Install dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
./setup.sh --new-env --basic --flash-attn --xformers

# Test installation
python test_installation.py
```

#### Expected Output
- ✅ TRELLIS model loads successfully
- ✅ GPU recognized (24GB VRAM available)
- ✅ Test image processes in 15-30 seconds
- ✅ Output GLB/STL files generated

#### Success Criteria
- Single image → STL in under 30 seconds
- VRAM usage stays under 18GB
- No CUDA errors

#### Documentation to Read
- https://github.com/microsoft/TRELLIS/README.md
- https://github.com/microsoft/TRELLIS/docs/installation.md
- CUDA installation guide for Fedora

---

### TASK_002: TRELLIS Integration Test
**Phase**: 1 | **Week**: 1 | **Days**: 3-4 | **Time**: 12 hours

#### Description
Create working Python pipeline that takes images and outputs STL files using TRELLIS.

#### Steps
1. Write image loading function
2. Implement TRELLIS inference
3. Extract mesh from outputs
4. Export to GLB format
5. Test with diverse images

#### Archon Research Queries
```bash
archon query "TRELLIS multi-image input format"
archon query "TRELLIS output formats Gaussian mesh radiance"
archon query "TRELLIS post-processing utilities"
archon query "Convert GLB to STL Python"
```

#### Implementation
```python
# core/trellis_pipeline.py
from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import postprocessing_utils
from PIL import Image

class TRELLISProcessor:
    def __init__(self, model_name="microsoft/TRELLIS-image-large"):
        self.pipeline = TrellisImageTo3DPipeline.from_pretrained(model_name)
        self.pipeline.cuda()
    
    def process_single_image(self, image_path: str, output_path: str):
        """Quick tier: 1 image → STL"""
        image = Image.open(image_path)
        
        outputs = self.pipeline.run(
            image,
            seed=42,
            sparse_structure_sampler_params={"steps": 12},
            slat_sampler_params={"steps": 12}
        )
        
        glb = postprocessing_utils.to_glb(
            outputs['gaussian'][0],
            outputs['mesh'][0],
            simplify=0.95,
            texture_size=1024
        )
        
        glb.export(output_path)
        return output_path
    
    def process_multi_image(self, image_paths: list, output_path: str):
        """Standard/Pro tier: multiple images → STL"""
        images = [Image.open(p) for p in image_paths]
        
        outputs = self.pipeline.run(
            images,
            seed=42,
            sparse_structure_sampler_params={"steps": 16},
            slat_sampler_params={"steps": 16}
        )
        
        glb = postprocessing_utils.to_glb(
            outputs['gaussian'][0],
            outputs['mesh'][0],
            simplify=0.95,
            texture_size=1024
        )
        
        glb.export(output_path)
        return output_path

# Test script
if __name__ == "__main__":
    processor = TRELLISProcessor()
    
    # Test single image
    processor.process_single_image("test_data/sample.jpg", "output/quick.glb")
    
    # Test multi image
    processor.process_multi_image(
        ["test_data/img1.jpg", "test_data/img2.jpg", "test_data/img3.jpg"],
        "output/pro.glb"
    )
```

#### Expected Output
- ✅ Working Python class
- ✅ Single-image processing: 15-30 seconds
- ✅ Multi-image processing: 2-3 minutes
- ✅ GLB files exported successfully

#### Success Criteria
- 10 test images all process successfully
- Visual inspection confirms 3D quality
- VRAM usage documented

#### Pitfalls to Watch
- **Cold start time**: First run slower (model loading)
- **Image preprocessing**: Ensure images are properly formatted
- **Memory leaks**: Clear VRAM between runs

---

### TASK_003: FreeCAD STL Validation
**Phase**: 1 | **Week**: 1 | **Days**: 5-7 | **Time**: 16 hours

#### Description
Integrate FreeCAD Python API to validate meshes and export print-ready STL files.

#### Steps
1. Install FreeCAD with Python bindings
2. Write mesh validation function
3. Implement repair algorithms
4. Test watertight checking
5. Validate scale for 3D printing

#### Archon Research Queries
```bash
archon query "FreeCAD Python API mesh import"
archon query "FreeCAD mesh validation watertight"
archon query "FreeCAD mesh repair algorithms"
archon query "STL export best practices 3D printing"
archon query "Mesh non-manifold geometry fix"
```

#### Implementation
```python
# core/freecad_processor.py
import FreeCAD
import Mesh
import MeshPart
from pathlib import Path

class FreeCADProcessor:
    def validate_and_export(self, glb_path: str, output_stl: str) -> dict:
        """
        Validate mesh and export STL for 3D printing
        """
        doc = FreeCAD.newDocument("MeshProcessing")
        
        # Import GLB as mesh
        mesh_obj = self._import_glb(doc, glb_path)
        mesh = mesh_obj.Mesh
        
        # Run validations
        checks = {
            "is_solid": mesh.isSolid(),
            "has_non_manifolds": mesh.hasNonManifolds(),
            "has_self_intersections": mesh.hasSelfIntersections(),
            "vertex_count": len(mesh.Points),
            "triangle_count": len(mesh.Facets)
        }
        
        # Repair if needed
        if not checks["is_solid"] or checks["has_non_manifolds"]:
            self._repair_mesh(mesh)
            checks["repaired"] = True
        
        # Export STL
        mesh.write(output_stl)
        
        # Calculate dimensions
        bbox = mesh.BoundBox
        checks["dimensions_mm"] = {
            "x": bbox.XLength,
            "y": bbox.YLength,
            "z": bbox.ZLength
        }
        
        FreeCAD.closeDocument(doc.Name)
        
        return checks
    
    def _import_glb(self, doc, glb_path):
        """Import GLB file"""
        # FreeCAD doesn't natively support GLB
        # Convert GLB to OBJ first
        mesh_obj = doc.addObject("Mesh::Feature", "Model")
        # Use trimesh or another library to convert
        return mesh_obj
    
    def _repair_mesh(self, mesh):
        """Repair common mesh issues"""
        # Harmonize normals
        if mesh.hasNonUniformOrientedFacets():
            mesh.harmonizeNormals()
        
        # Remove duplicates
        mesh.removeDuplicatedPoints()
        mesh.removeDuplicatedFacets()
        
        # Fill holes
        mesh.fillupHoles(10.0)
        
        # Remove non-manifold edges
        mesh.removeNonManifolds()

# Test script
if __name__ == "__main__":
    processor = FreeCADProcessor()
    
    result = processor.validate_and_export(
        "output/quick.glb",
        "output/validated.stl"
    )
    
    print(f"Validation results: {result}")
```

#### Expected Output
- ✅ FreeCAD processes meshes successfully
- ✅ STL files are watertight
- ✅ Validation report generated
- ✅ Repair algorithms work

#### Success Criteria
- 100% of TRELLIS outputs pass validation
- Repaired meshes are printable
- STL scale is correct (mm)

#### Pitfalls to Watch
- **GLB conversion**: May need intermediate format
- **Scale issues**: Ensure units are millimeters
- **Non-manifold geometry**: May require manual fixes

---

## Complete Task List Summary

### Week 1
- [x] TASK_001: Development Environment (Days 1-2)
- [x] TASK_002: TRELLIS Integration (Days 3-4)
- [x] TASK_003: FreeCAD Validation (Days 5-7)

### Week 2  
- [ ] TASK_004: Medusa Installation (Days 8-9)
- [ ] TASK_005: Custom Processing Module (Days 10-12)
- [ ] TASK_006: Product Configuration (Days 13-14)

### Week 3
- [ ] TASK_007: Docker Image (Days 15-17)
- [ ] TASK_008: RunPod Handler (Days 18-21)

### Week 4
- [ ] TASK_009: FastAPI Orchestrator (Days 22-24)
- [ ] TASK_010: Security Implementation (Days 25-28)

### Week 5
- [ ] TASK_011: Next.js Storefront (Days 29-31)
- [ ] TASK_012: Upload Component (Days 32-33)
- [ ] TASK_013: Job Status Page (Days 34-35)

### Week 6
- [ ] TASK_014: Admin Widgets (Days 36-38)
- [ ] TASK_015: Monitoring Dashboard (Days 39-42)

### Week 7
- [ ] TASK_016: Testing Suite (Days 43-45)
- [ ] TASK_017: Performance Benchmark (Days 46-49)

### Week 8
- [ ] TASK_018: Security Audit (Days 50-52)
- [ ] TASK_019: Production Deployment (Days 53-56)

### Week 9+
- [ ] TASK_020: Beta Testing (Days 57-60)
- [ ] TASK_021: Public Launch (Days 61+)

---

## Task Dependencies Graph

```
TASK_001 (Setup)
  ↓
TASK_002 (TRELLIS) → TASK_003 (FreeCAD)
  ↓                      ↓
TASK_004 (Medusa)    TASK_007 (Docker)
  ↓                      ↓
TASK_005 (Module)    TASK_008 (RunPod)
  ↓                      ↓
TASK_006 (Products)  TASK_009 (FastAPI) → TASK_010 (Security)
  ↓                      ↓
TASK_011 (Frontend)  ←──┘
  ↓
TASK_012 (Upload) → TASK_013 (Status)
  ↓
TASK_014 (Admin) → TASK_015 (Monitoring)
  ↓
TASK_016 (Testing) → TASK_017 (Performance)
  ↓
TASK_018 (Security Audit) → TASK_019 (Deployment)
  ↓
TASK_020 (Beta) → TASK_021 (Launch)
```

---

## Archon MCP Usage

### How to Use Archon for Each Task

1. **Before starting task**: Query documentation
   ```bash
   archon index-repo https://github.com/microsoft/TRELLIS
   archon query "TRELLIS installation requirements"
   ```

2. **During implementation**: Query specific issues
   ```bash
   archon query "TRELLIS multi-image API usage example"
   archon query "Common TRELLIS VRAM issues"
   ```

3. **When stuck**: Search error messages
   ```bash
   archon query "TRELLIS CUDA out of memory fix"
   archon query "FreeCAD mesh repair examples"
   ```

### Archon Project Setup

```bash
# Initialize Archon project
archon create-project "3d-print-mvp"

# Index all repositories
archon index-repo https://github.com/microsoft/TRELLIS
archon index-repo https://github.com/Anttwo/SuGaR
archon index-repo https://github.com/medusajs/medusa

# Create tasks
archon create-task "TASK_001" "Setup TRELLIS environment"
archon link-docs "TASK_001" "https://github.com/microsoft/TRELLIS/README.md"
```

---

## Time Tracking Template

```markdown
### Task: TASK_XXX
**Started**: YYYY-MM-DD HH:MM
**Completed**: YYYY-MM-DD HH:MM
**Actual Time**: X hours
**Estimated Time**: Y hours
**Variance**: +/- Z hours

**Notes**:
- What went well
- What took longer than expected
- Lessons learned
```

---

*See individual phase files (PHASE_1.md, PHASE_2.md, etc.) for detailed task breakdowns.*
