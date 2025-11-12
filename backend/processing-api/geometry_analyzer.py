"""
Geometry Analysis for Manufacturing Recommendations
Analyzes 3D models to suggest optimal manufacturing method
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManufacturingMethod(str, Enum):
    """Manufacturing methods"""
    FDM = "fdm"
    SLS = "sls"
    CFC = "cfc"
    CNC = "cnc"

@dataclass
class GeometryFeatures:
    """Extracted geometry features"""
    # Dimensions (mm)
    bounding_box: Tuple[float, float, float]  # (x, y, z)
    volume: float  # mm³
    surface_area: float  # mm²

    # Geometric complexity
    has_overhangs: bool
    max_overhang_angle: float  # degrees
    has_thin_walls: bool
    min_wall_thickness: float  # mm
    has_complex_geometry: bool
    complexity_score: float  # 0-1

    # Internal features
    has_internal_cavities: bool
    has_internal_channels: bool
    requires_supports: bool

    # Surface characteristics
    surface_roughness_requirement: str  # "low", "medium", "high"
    dimensional_tolerance: str  # "loose", "standard", "tight"

@dataclass
class ManufacturingRecommendation:
    """Manufacturing method recommendation"""
    method: ManufacturingMethod
    confidence: float  # 0-1
    reasoning: str
    pros: List[str]
    cons: List[str]
    estimated_cost: float  # £
    estimated_time: str
    material_suggestion: str

class GeometryAnalyzer:
    """Analyzes geometry and recommends manufacturing methods"""

    # Build volume limits (mm)
    BUILD_VOLUMES = {
        ManufacturingMethod.FDM: (250, 210, 210),  # Prusa i3 MK3S
        ManufacturingMethod.SLS: (350, 350, 600),  # EOS P110
        ManufacturingMethod.CFC: (320, 132, 154),  # Markforged X7
        ManufacturingMethod.CNC: (400, 300, 200),  # Generic CNC
    }

    # Cost factors (£ base + £/cm³)
    COST_FACTORS = {
        ManufacturingMethod.FDM: (10, 0.05),
        ManufacturingMethod.SLS: (30, 0.15),
        ManufacturingMethod.CFC: (80, 0.40),
        ManufacturingMethod.CNC: (100, 0.50),
    }

    def __init__(self):
        pass

    def analyze_geometry(self, mesh_data: Dict[str, Any]) -> GeometryFeatures:
        """
        Analyze 3D mesh geometry

        Args:
            mesh_data: Dictionary with mesh analysis data
                {
                    'bounding_box': [x, y, z],
                    'volume': float,
                    'surface_area': float,
                    'has_overhangs': bool,
                    'min_wall_thickness': float,
                    ...
                }

        Returns:
            GeometryFeatures object
        """

        # Extract features from mesh data
        # In production, this would use actual mesh analysis libraries
        # like trimesh, pyvista, or Open3D

        features = GeometryFeatures(
            bounding_box=tuple(mesh_data.get('bounding_box', [0, 0, 0])),
            volume=mesh_data.get('volume', 0),
            surface_area=mesh_data.get('surface_area', 0),
            has_overhangs=mesh_data.get('has_overhangs', False),
            max_overhang_angle=mesh_data.get('max_overhang_angle', 0),
            has_thin_walls=mesh_data.get('has_thin_walls', False),
            min_wall_thickness=mesh_data.get('min_wall_thickness', 2.0),
            has_complex_geometry=mesh_data.get('has_complex_geometry', False),
            complexity_score=mesh_data.get('complexity_score', 0.5),
            has_internal_cavities=mesh_data.get('has_internal_cavities', False),
            has_internal_channels=mesh_data.get('has_internal_channels', False),
            requires_supports=mesh_data.get('requires_supports', False),
            surface_roughness_requirement=mesh_data.get('surface_roughness', 'medium'),
            dimensional_tolerance=mesh_data.get('tolerance', 'standard')
        )

        logger.info(f"📊 Analyzed geometry: {features.bounding_box} mm, {features.volume:.2f} mm³")
        return features

    def recommend_method(self, features: GeometryFeatures) -> List[ManufacturingRecommendation]:
        """
        Recommend manufacturing methods based on geometry

        Returns:
            List of recommendations sorted by confidence (highest first)
        """

        recommendations = []

        # Analyze suitability for each method
        recommendations.append(self._evaluate_fdm(features))
        recommendations.append(self._evaluate_sls(features))
        recommendations.append(self._evaluate_cfc(features))
        recommendations.append(self._evaluate_cnc(features))

        # Sort by confidence
        recommendations.sort(key=lambda x: x.confidence, reverse=True)

        logger.info(f"🎯 Top recommendation: {recommendations[0].method.value} ({recommendations[0].confidence:.0%} confidence)")

        return recommendations

    def _evaluate_fdm(self, features: GeometryFeatures) -> ManufacturingRecommendation:
        """Evaluate suitability for FDM printing"""

        confidence = 0.5  # Start neutral
        pros = []
        cons = []

        # Check build volume
        if self._fits_build_volume(features, ManufacturingMethod.FDM):
            confidence += 0.1
            pros.append("Fits within FDM build volume")
        else:
            confidence -= 0.3
            cons.append("Exceeds FDM build volume")

        # Check overhangs
        if not features.has_overhangs:
            confidence += 0.15
            pros.append("No overhangs - minimal supports needed")
        else:
            confidence -= 0.1
            cons.append("Overhangs require support structures")

        # Check wall thickness
        if features.min_wall_thickness >= 1.2:
            confidence += 0.1
            pros.append("Wall thickness suitable for FDM")
        else:
            confidence -= 0.2
            cons.append("Thin walls may be challenging with FDM")

        # Check complexity
        if features.complexity_score < 0.6:
            confidence += 0.15
            pros.append("Simple geometry ideal for FDM")
        else:
            confidence -= 0.05
            cons.append("Complex geometry - may have visible layer lines")

        # Tolerance requirements
        if features.dimensional_tolerance == "loose":
            confidence += 0.1
            pros.append("Tolerance requirements match FDM capabilities")
        elif features.dimensional_tolerance == "tight":
            confidence -= 0.15
            cons.append("FDM may not achieve tight tolerances")

        # Always add cost and speed as pros
        pros.append("Fastest turnaround (same day)")
        pros.append("Most cost-effective option")

        # Estimate cost
        cost = self._estimate_cost(features, ManufacturingMethod.FDM)

        return ManufacturingRecommendation(
            method=ManufacturingMethod.FDM,
            confidence=max(0.0, min(1.0, confidence)),
            reasoning=self._generate_reasoning(features, "FDM", confidence),
            pros=pros,
            cons=cons,
            estimated_cost=cost,
            estimated_time="4-8 hours (same day)",
            material_suggestion="PLA or PETG"
        )

    def _evaluate_sls(self, features: GeometryFeatures) -> ManufacturingRecommendation:
        """Evaluate suitability for SLS printing"""

        confidence = 0.5
        pros = []
        cons = []

        # Check build volume
        if self._fits_build_volume(features, ManufacturingMethod.SLS):
            confidence += 0.1
            pros.append("Fits within SLS build volume")
        else:
            confidence -= 0.3
            cons.append("Exceeds SLS build volume")

        # SLS handles overhangs well (self-supporting)
        if features.has_overhangs:
            confidence += 0.15
            pros.append("No supports needed - powder acts as support")

        # Complex geometry
        if features.complexity_score > 0.5:
            confidence += 0.2
            pros.append("Excellent for complex geometries")

        # Internal features
        if features.has_internal_cavities or features.has_internal_channels:
            confidence += 0.15
            pros.append("Can produce internal features without supports")

        # Wall thickness
        if features.min_wall_thickness >= 0.8:
            confidence += 0.1
            pros.append("Wall thickness suitable for SLS")
        else:
            confidence -= 0.1
            cons.append("Very thin walls may be fragile")

        # Functional parts
        if features.complexity_score > 0.4:
            confidence += 0.1
            pros.append("Good mechanical properties for functional testing")

        # Always note
        pros.append("No support structures needed")
        pros.append("Good surface finish")
        cons.append("Longer turnaround than FDM (1-2 days)")
        cons.append("Requires depowdering post-processing")

        cost = self._estimate_cost(features, ManufacturingMethod.SLS)

        return ManufacturingRecommendation(
            method=ManufacturingMethod.SLS,
            confidence=max(0.0, min(1.0, confidence)),
            reasoning=self._generate_reasoning(features, "SLS", confidence),
            pros=pros,
            cons=cons,
            estimated_cost=cost,
            estimated_time="1-2 days",
            material_suggestion="PA12 (Nylon)"
        )

    def _evaluate_cfc(self, features: GeometryFeatures) -> ManufacturingRecommendation:
        """Evaluate suitability for CFC (Continuous Fiber Composite) printing"""

        confidence = 0.4  # Start lower - more specialized
        pros = []
        cons = []

        # Check build volume
        if self._fits_build_volume(features, ManufacturingMethod.CFC):
            confidence += 0.1
            pros.append("Fits within CFC build volume")
        else:
            confidence -= 0.4
            cons.append("Exceeds CFC build volume")
            return self._create_low_confidence_cfc(cons)

        # Best for load-bearing parts
        if features.complexity_score > 0.6 and features.surface_area > 10000:
            confidence += 0.2
            pros.append("Complex geometry with high surface area - ideal for fiber reinforcement")

        # Strength requirements
        if features.dimensional_tolerance == "tight":
            confidence += 0.15
            pros.append("CFC can achieve tight tolerances with proper planning")

        # Wall thickness
        if features.min_wall_thickness >= 1.5:
            confidence += 0.1
            pros.append("Wall thickness allows for fiber layers")
        else:
            confidence -= 0.15
            cons.append("Thin walls challenging for fiber reinforcement")

        pros.append("Highest strength-to-weight ratio")
        pros.append("End-use part quality")
        cons.append("Requires STEP file refinement and fiber planning")
        cons.append("Longest turnaround (2-3 days)")
        cons.append("Highest cost")

        cost = self._estimate_cost(features, ManufacturingMethod.CFC)

        return ManufacturingRecommendation(
            method=ManufacturingMethod.CFC,
            confidence=max(0.0, min(1.0, confidence)),
            reasoning=self._generate_reasoning(features, "CFC", confidence),
            pros=pros,
            cons=cons,
            estimated_cost=cost,
            estimated_time="2-3 days (includes fiber planning)",
            material_suggestion="Onyx + Carbon Fiber"
        )

    def _evaluate_cnc(self, features: GeometryFeatures) -> ManufacturingRecommendation:
        """Evaluate suitability for CNC machining"""

        confidence = 0.4
        pros = []
        cons = []

        # Check build volume
        if self._fits_build_volume(features, ManufacturingMethod.CNC):
            confidence += 0.1
            pros.append("Fits within CNC work envelope")
        else:
            confidence -= 0.4
            cons.append("Exceeds CNC work envelope")
            return self._create_low_confidence_cnc(cons)

        # Best for tight tolerances
        if features.dimensional_tolerance == "tight":
            confidence += 0.25
            pros.append("CNC excels at tight tolerances (±0.01mm possible)")

        # Surface finish
        if features.surface_roughness_requirement == "high":
            confidence += 0.15
            pros.append("Excellent surface finish capabilities")

        # Complexity penalty
        if features.complexity_score > 0.7:
            confidence -= 0.15
            cons.append("High complexity increases machining time and cost")
        if features.has_internal_cavities:
            confidence -= 0.1
            cons.append("Internal cavities require special tooling")

        # Simple geometries work best
        if features.complexity_score < 0.5:
            confidence += 0.15
            pros.append("Simple geometry well-suited for CNC")

        pros.append("Best dimensional accuracy")
        pros.append("Wide material selection")
        cons.append("Requires CAM planning")
        cons.append("Higher cost than FDM/SLS")

        cost = self._estimate_cost(features, ManufacturingMethod.CNC)

        return ManufacturingRecommendation(
            method=ManufacturingMethod.CNC,
            confidence=max(0.0, min(1.0, confidence)),
            reasoning=self._generate_reasoning(features, "CNC", confidence),
            pros=pros,
            cons=cons,
            estimated_cost=cost,
            estimated_time="1-2 days (includes CAM planning)",
            material_suggestion="Aluminum 6061 or ABS stock"
        )

    def _fits_build_volume(self, features: GeometryFeatures, method: ManufacturingMethod) -> bool:
        """Check if part fits in build volume"""
        max_x, max_y, max_z = self.BUILD_VOLUMES[method]
        part_x, part_y, part_z = features.bounding_box

        return part_x <= max_x and part_y <= max_y and part_z <= max_z

    def _estimate_cost(self, features: GeometryFeatures, method: ManufacturingMethod) -> float:
        """Estimate manufacturing cost"""
        base_cost, cost_per_cm3 = self.COST_FACTORS[method]

        # Convert volume to cm³
        volume_cm3 = features.volume / 1000

        # Calculate cost
        total_cost = base_cost + (volume_cm3 * cost_per_cm3)

        # Complexity multiplier
        complexity_multiplier = 1.0 + (features.complexity_score * 0.5)
        total_cost *= complexity_multiplier

        return round(total_cost, 2)

    def _generate_reasoning(self, features: GeometryFeatures, method: str, confidence: float) -> str:
        """Generate reasoning text"""

        x, y, z = features.bounding_box
        volume_cm3 = features.volume / 1000

        if confidence > 0.7:
            rating = "Highly recommended"
        elif confidence > 0.5:
            rating = "Good fit"
        elif confidence > 0.3:
            rating = "Possible but not ideal"
        else:
            rating = "Not recommended"

        reasoning = f"{rating} for {method}. "
        reasoning += f"Part dimensions: {x:.1f} × {y:.1f} × {z:.1f} mm, "
        reasoning += f"volume: {volume_cm3:.2f} cm³. "

        if features.has_overhangs:
            reasoning += "Has overhangs. "
        if features.has_complex_geometry:
            reasoning += "Complex geometry detected. "
        if features.dimensional_tolerance == "tight":
            reasoning += "Tight tolerances required. "

        return reasoning.strip()

    def _create_low_confidence_cfc(self, cons: List[str]) -> ManufacturingRecommendation:
        """Create low-confidence CFC recommendation"""
        return ManufacturingRecommendation(
            method=ManufacturingMethod.CFC,
            confidence=0.1,
            reasoning="Part exceeds CFC build volume or is not suitable for fiber reinforcement",
            pros=["Highest strength possible"],
            cons=cons,
            estimated_cost=0.0,
            estimated_time="N/A",
            material_suggestion="N/A"
        )

    def _create_low_confidence_cnc(self, cons: List[str]) -> ManufacturingRecommendation:
        """Create low-confidence CNC recommendation"""
        return ManufacturingRecommendation(
            method=ManufacturingMethod.CNC,
            confidence=0.1,
            reasoning="Part not suitable for CNC machining",
            pros=["Best accuracy"],
            cons=cons,
            estimated_cost=0.0,
            estimated_time="N/A",
            material_suggestion="N/A"
        )


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def example_analysis():
    """Example geometry analysis"""

    analyzer = GeometryAnalyzer()

    # Sample mesh data (in production, this comes from actual mesh analysis)
    mesh_data = {
        'bounding_box': [80, 60, 40],  # mm
        'volume': 150000,  # mm³
        'surface_area': 25000,  # mm²
        'has_overhangs': False,
        'max_overhang_angle': 0,
        'has_thin_walls': False,
        'min_wall_thickness': 2.5,
        'has_complex_geometry': True,
        'complexity_score': 0.6,
        'has_internal_cavities': True,
        'has_internal_channels': False,
        'requires_supports': False,
        'surface_roughness': 'medium',
        'tolerance': 'standard'
    }

    # Analyze geometry
    features = analyzer.analyze_geometry(mesh_data)

    # Get recommendations
    recommendations = analyzer.recommend_method(features)

    # Print results
    print("\n" + "="*60)
    print("MANUFACTURING RECOMMENDATIONS")
    print("="*60)

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.method.value.upper()} - {rec.confidence:.0%} confidence")
        print(f"   Cost: £{rec.estimated_cost:.2f}")
        print(f"   Time: {rec.estimated_time}")
        print(f"   Material: {rec.material_suggestion}")
        print(f"\n   Reasoning: {rec.reasoning}")
        print(f"\n   ✅ Pros:")
        for pro in rec.pros:
            print(f"      • {pro}")
        print(f"\n   ❌ Cons:")
        for con in rec.cons:
            print(f"      • {con}")


if __name__ == "__main__":
    example_analysis()
