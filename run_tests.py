#!/usr/bin/env python3
"""
Test runner script that provides convenient shortcuts for running tests with Allure reporting.
"""
import os
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Run tests with preconfigured options")
    
    # Test selection options
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--regression", action="store_true", help="Run regression tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--ui", action="store_true", help="Run UI tests")
    
    # Browser options
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge", "safari"], 
                        default="chrome", help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--remote", action="store_true", help="Use remote WebDriver")
    
    # Extra pytest options
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", type=int, help="Number of parallel processes")
    parser.add_argument("path", nargs="*", help="Path(s) to test files or directories")
    
    args = parser.parse_args()
    
    # Create allure-results directory if it doesn't exist
    if not os.path.exists("allure-results"):
        os.makedirs("allure-results")
    
    # Build pytest command
    pytest_args = ["pytest"]
    
    # Add Allure reporting
    pytest_args.append("--alluredir=allure-results")
    
    # Handle test selection
    if args.smoke:
        pytest_args.append("-m smoke")
    elif args.regression:
        pytest_args.append("-m regression")
    elif args.api:
        pytest_args.append("-m api")
    elif args.ui:
        pytest_args.append("-m ui")
    # No marker means run all tests
    
    # Add browser options
    pytest_args.append(f"--browser={args.browser}")
    if args.headless:
        pytest_args.append("--headless")
    if args.remote:
        pytest_args.append("--remote")
    
    # Add verbosity
    if args.verbose:
        pytest_args.append("-v")
    
    # Add parallel execution
    if args.parallel:
        pytest_args.append(f"-n {args.parallel}")
    
    # Add test paths if specified
    if args.path:
        pytest_args.extend(args.path)
    
    # Join all arguments into a command string
    command = " ".join(pytest_args)
    print(f"Running: {command}")
    
    # Run the command
    result = subprocess.run(command, shell=True)
    
    print("\nTest execution completed.")
    print(f"Allure results saved to: {os.path.abspath('allure-results')}")
    print("To view the report, run: allure serve allure-results")
    
    # Exit with the same code
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
