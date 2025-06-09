"""
Configuration for VLSI RAG testing with OpenROAD
"""
import os

# Test output directory
TEST_OUTPUT_DIR = 'test_outputs'
if not os.path.exists(TEST_OUTPUT_DIR):
    os.makedirs(TEST_OUTPUT_DIR)

# Verification points (files that should exist after certain steps)
VERIFICATION_POINTS = {
    'post_floorplan': os.path.join(TEST_OUTPUT_DIR, 'floorplan.def'),
    'post_placement': os.path.join(TEST_OUTPUT_DIR, 'placement.def'),
    'post_cts': os.path.join(TEST_OUTPUT_DIR, 'cts.def'),
    'post_routing': os.path.join(TEST_OUTPUT_DIR, 'routing.def'),
    'timing_reports': os.path.join(TEST_OUTPUT_DIR, 'timing_reports'),
    'power_reports': os.path.join(TEST_OUTPUT_DIR, 'power_reports')
}

# Test design configurations
TEST_DESIGNS = {
    'gcd': {
        'name': 'gcd',
        'die_area': '0 0 100 100',
        'core_area': '10 10 90 90',
        'target_utilization': 0.5,
        'aspect_ratio': 1.0,
        'core_margin': 2.0
    }
} 