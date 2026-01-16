import subprocess
import sys
import os

def test_brain_reasoning_script_imports_correctly():
    """
    Verifies that src/brain_reasoning.py can be executed without ModuleNotFoundError.
    It may fail due to missing data or keys, but it should not fail with import errors.
    """
    # Run the script as a separate process
    result = subprocess.run(
        [sys.executable, "src/brain_reasoning.py"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    # Check stderr for ModuleNotFoundError
    # The script currently fails with "ModuleNotFoundError: No module named 'src'"
    # We want to assert that this specific error is NOT present.
    # However, for the "Red" phase, we expect it to fail (or rather, we want to prove it fails).
    # Since we want to pass the test when it's fixed, we should assert success or specific exit code?
    # No, let's assert that the output DOES NOT contain ModuleNotFoundError.
    
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # If the bug exists, this assertion will fail (because stderr contains the error)
    # Wait, if I want to write a failing test, I should write a test that expects Success, and it will fail.
    
    # The script should theoretically run (even if it does nothing due to missing data).
    # If it crashes with ImportError, return code will be != 0.
    
    # To be precise: The current bug causes a crash.
    # We want a test that says "It should not crash with ImportError".
    
    assert "ModuleNotFoundError" not in result.stderr
    # Also ideally exit code should be 0, but it might exit with non-zero if no data found?
    # Looking at main(): it logs error "No data available" but doesn't explicitly sys.exit(1).
    # So it should exit 0.
    assert result.returncode == 0
