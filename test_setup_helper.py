"""
Helper functions for setting up and verifying VLSI RAG tests
"""
import os
import subprocess
from typing import Dict, Optional, List
from test_config import (
    PLATFORM_CONFIG,
    DESIGN_CONFIG,
    TEST_OUTPUT_DIR,
    VERIFICATION_POINTS,
    OPENROAD_SCRIPTS,
    TEST_DESIGNS
)

def verify_openroad_installation() -> bool:
    """Verify OpenROAD is installed and accessible"""
    try:
        subprocess.run(['openroad', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def verify_design_files(design_name: str = 'gcd') -> Dict[str, bool]:
    """Verify all necessary design files exist"""
    design_config = TEST_DESIGNS[design_name]
    files_to_check = {
        'lef': PLATFORM_CONFIG['lef_file'],
        'tech_lef': PLATFORM_CONFIG['tech_lef'],
        'lib': PLATFORM_CONFIG['lib_file'],
        'rtl': DESIGN_CONFIG['rtl_file'],
        'sdc': DESIGN_CONFIG['sdc_file']
    }
    
    return {name: os.path.exists(path) for name, path in files_to_check.items()}

def setup_test_design(design_name: str = 'gcd') -> Optional[str]:
    """
    Set up a test design for RAG testing
    Returns: Path to the loaded design DEF file or None if setup fails
    """
    # Create test output directory if it doesn't exist
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    # Create OpenROAD script for design setup
    setup_script = os.path.join(TEST_OUTPUT_DIR, 'setup.tcl')
    design_config = TEST_DESIGNS[design_name]
    
    with open(setup_script, 'w') as f:
        f.write(f"""
# Read technology files
read_lef {PLATFORM_CONFIG['tech_lef']}
read_lef {PLATFORM_CONFIG['lef_file']}
read_liberty {PLATFORM_CONFIG['lib_file']}

# Read design
read_verilog {DESIGN_CONFIG['rtl_file']}
link_design {design_config['name']}

# Initialize floorplan
initialize_floorplan \\
    -die_area "{design_config['die_area']}" \\
    -core_area "{design_config['core_area']}" \\
    -utilization {design_config['target_utilization']} \\
    -aspect_ratio {design_config['aspect_ratio']} \\
    -core_margin {design_config['core_margin']}

# Read constraints
read_sdc {DESIGN_CONFIG['sdc_file']}

# Initialize power grid
source {OPENROAD_SCRIPTS['floorplan']}

# Write output
write_def {VERIFICATION_POINTS['post_floorplan']}
exit
""")
    
    # Run OpenROAD with setup script
    try:
        subprocess.run(['openroad', setup_script], capture_output=True, check=True)
        return VERIFICATION_POINTS['post_floorplan'] if os.path.exists(VERIFICATION_POINTS['post_floorplan']) else None
    except subprocess.CalledProcessError:
        return None

def verify_design_setup() -> Dict[str, bool]:
    """Verify design setup by checking output files"""
    return {
        name: os.path.exists(path)
        for name, path in VERIFICATION_POINTS.items()
    }

def cleanup_test_outputs():
    """Clean up test output directory"""
    import shutil
    if os.path.exists(TEST_OUTPUT_DIR):
        shutil.rmtree(TEST_OUTPUT_DIR)

def get_design_state() -> Dict[str, str]:
    """Get current state of the design setup"""
    state = {}
    
    # Check if design is loaded
    if os.path.exists(VERIFICATION_POINTS['post_floorplan']):
        state['design_loaded'] = 'yes'
        state['current_def'] = VERIFICATION_POINTS['post_floorplan']
    else:
        state['design_loaded'] = 'no'
        state['current_def'] = None
    
    # Check design stage
    for stage in ['post_floorplan', 'post_placement', 'post_cts', 'post_routing']:
        if os.path.exists(VERIFICATION_POINTS[stage]):
            state['current_stage'] = stage
            break
    else:
        state['current_stage'] = 'none'
    
    return state

def get_available_commands(stage: str) -> List[str]:
    """Get list of available commands based on design stage"""
    common_commands = [
        'read_lef',
        'read_def',
        'write_def',
        'get_cells',
        'get_nets',
        'get_pins'
    ]
    
    stage_commands = {
        'post_floorplan': [
            'place_pins',
            'initialize_floorplan',
            'make_tracks'
        ],
        'post_placement': [
            'global_placement',
            'detailed_placement',
            'optimize_placement'
        ],
        'post_cts': [
            'clock_tree_synthesis',
            'report_clock_skew',
            'repair_clock_nets'
        ],
        'post_routing': [
            'detailed_route',
            'repair_design',
            'report_routing'
        ]
    }
    
    return common_commands + stage_commands.get(stage, []) 