"""
Day 4 Labs Automation Script
Executes Lab 1 (Testing) and Lab 2 (CI/CD) requirements
"""
import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, 'c:/Workspace/AG-AISOFTDEV')

# Load environment variables manually
from dotenv import load_dotenv
load_dotenv('c:/Workspace/AG-AISOFTDEV/.env')

from utils import setup_llm_client, get_completion, load_artifact, save_artifact, clean_llm_output

def print_step(step_num, title):
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {title}")
    print('='*70)

def main():
    errors = []
    completed = []
    
    # Setup
    print_step(0, "INITIALIZATION")
    client, model_name, api_provider = setup_llm_client(model_name='gemini-2.5-pro')
    print(f"✓ LLM Client: {model_name} via {api_provider}")
    
    app_code = load_artifact('app/main.py')
    if not app_code:
        print("❌ FATAL: Could not load app/main.py")
        return
    print("✓ Loaded app/main.py")
    
    # LAB 1 CHALLENGE 1: Happy Path Tests
    print_step(1, "LAB 1 - CHALLENGE 1: Happy Path Tests")
    try:
        happy_prompt = f"""Act as a QA Engineer. Generate pytest tests for this FastAPI app:

{app_code}

Create tests for:
1. POST /users/ - assert 201 status and valid response body
2. GET /users/ - assert 200 status and list response

Use FastAPI TestClient. Include all necessary imports. Return only clean Python code."""
        
        print("Generating tests...")
        happy_tests = get_completion(happy_prompt, client, model_name, api_provider)
        happy_tests_clean = clean_llm_output(happy_tests, 'python')
        
        save_artifact(happy_tests_clean, 'tests/test_main_simple.py', overwrite=True)
        print("✅ Saved tests/test_main_simple.py")
        completed.append("Lab 1 Challenge 1 - Happy Path Tests")
    except Exception as e:
        errors.append(f"Lab 1 Challenge 1: {str(e)}")
        print(f"❌ Error: {e}")
    
    # LAB 1 CHALLENGE 2: Edge Case Tests
    print_step(2, "LAB 1 - CHALLENGE 2: Edge Case Tests")
    try:
        edge_prompt = f"""Generate pytest edge case tests for this FastAPI app:

{app_code}

Create tests for:
1. POST /users/ with duplicate email - expect 400 error
2. GET /users/{{user_id}} with non-existent ID - expect 404 error

Use FastAPI TestClient. Return only clean Python code."""
        
        print("Generating edge case tests...")
        edge_tests = get_completion(edge_prompt, client, model_name, api_provider)
        edge_tests_clean = clean_llm_output(edge_tests, 'python')
        
        print("--- Edge Case Tests ---")
        print(edge_tests_clean[:600])
        print("✅ Generated (not saved separately per instructions)")
        completed.append("Lab 1 Challenge 2 - Edge Case Tests")
    except Exception as e:
        errors.append(f"Lab 1 Challenge 2: {str(e)}")
        print(f"❌ Error: {e}")
    
    # LAB 1 CHALLENGE 3: Database Fixture
    print_step(3, "LAB 1 - CHALLENGE 3: Database Fixture")
    try:
        fixture_prompt = f"""Generate a pytest fixture for isolated database testing.

Application code:
{app_code}

Requirements:
- Configure temporary in-memory SQLite database using SQLAlchemy
- Create all tables before tests, tear down afterward
- Override the get_db dependency in the FastAPI app to use this temporary database
- Save as conftest.py

Return only clean Python code."""
        
        print("Generating database fixture...")
        fixture_code = get_completion(fixture_prompt, client, model_name, api_provider)
        fixture_clean = clean_llm_output(fixture_code, 'python')
        
        save_artifact(fixture_clean, 'tests/conftest.py', overwrite=True)
        print("✅ Saved tests/conftest.py")
        
        # Refactored tests
        refactor_prompt = f"""Rewrite the happy-path tests from test_main_simple.py to use the database fixture from conftest.py.

Original tests location: tests/test_main_simple.py
Fixture file: tests/conftest.py

Application code:
{app_code}

Return only clean Python code for the refactored tests."""
        
        print("Generating refactored tests...")
        refactor_tests = get_completion(refactor_prompt, client, model_name, api_provider)
        refactor_clean = clean_llm_output(refactor_tests, 'python')
        
        save_artifact(refactor_clean, 'tests/test_main_with_fixture.py', overwrite=True)
        print("✅ Saved tests/test_main_with_fixture.py")
        completed.append("Lab 1 Challenge 3 - Database Fixture")
    except Exception as e:
        errors.append(f"Lab 1 Challenge 3: {str(e)}")
        print(f"❌ Error: {e}")
    
    # LAB 1 VALIDATION: Run pytest
    print_step(4, "LAB 1 - VALIDATION: Run pytest")
    try:
        print("Running pytest...")
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/', '-v'],
            cwd='c:/Workspace/AG-AISOFTDEV',
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ All tests passed")
            completed.append("Lab 1 Validation - pytest")
        else:
            print(f"⚠️  Tests failed (exit code {result.returncode})")
            print("STDOUT:", result.stdout[:500])
            print("STDERR:", result.stderr[:500])
            
            # Retry once
            print("Retrying pytest...")
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', 'tests/', '-v'],
                cwd='c:/Workspace/AG-AISOFTDEV',
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print("✅ Tests passed on retry")
                completed.append("Lab 1 Validation - pytest (retry)")
            else:
                errors.append(f"Lab 1 Validation: pytest failed after retry")
                print("❌ Tests still failing after retry")
    except Exception as e:
        errors.append(f"Lab 1 Validation: {str(e)}")
        print(f"❌ Error running pytest: {e}")
    
    # LAB 2 CHALLENGE 1: requirements.txt
    print_step(5, "LAB 2 - CHALLENGE 1: requirements.txt")
    try:
        req_prompt = f"""Analyze this FastAPI application and generate a requirements.txt file:

{app_code}

Include:
- All application dependencies (fastapi, uvicorn, sqlalchemy, pydantic, etc.)
- pytest for testing
- Any other dependencies from imports

Return only the requirements.txt content, one package per line."""
        
        print("Generating requirements.txt...")
        requirements = get_completion(req_prompt, client, model_name, api_provider)
        requirements_clean = clean_llm_output(requirements, 'text')
        
        save_artifact(requirements_clean, 'requirements.txt', overwrite=True)
        print("✅ Saved requirements.txt")
        completed.append("Lab 2 Challenge 1 - requirements.txt")
    except Exception as e:
        errors.append(f"Lab 2 Challenge 1: {str(e)}")
        print(f"❌ Error: {e}")
    
    # LAB 2 CHALLENGE 2: Dockerfile
    print_step(6, "LAB 2 - CHALLENGE 2: Dockerfile")
    try:
        docker_prompt = """Generate a multi-stage Dockerfile for a Python FastAPI application.

Requirements:
- Base image: python:3.11-slim
- Stage 1: Install dependencies from requirements.txt
- Stage 2: Copy installed dependencies + application code
- CMD: Run app with uvicorn (command: uvicorn app.main:app --host 0.0.0.0 --port 8000)
- Expose port 8000

Return only the Dockerfile content."""
        
        print("Generating Dockerfile...")
        dockerfile = get_completion(docker_prompt, client, model_name, api_provider)
        dockerfile_clean = clean_llm_output(dockerfile, 'dockerfile')
        
        save_artifact(dockerfile_clean, 'Dockerfile', overwrite=True)
        print("✅ Saved Dockerfile")
        completed.append("Lab 2 Challenge 2 - Dockerfile")
    except Exception as e:
        errors.append(f"Lab 2 Challenge 2: {str(e)}")
        print(f"❌ Error: {e}")
    
    # LAB 2 CHALLENGE 3: GitHub Actions
    print_step(7, "LAB 2 - CHALLENGE 3: GitHub Actions Workflow")
    try:
        ci_prompt = """Generate a GitHub Actions workflow file (ci.yml) for CI/CD.

Requirements:
- Name: CI
- Trigger: push to main branch
- Job: build-and-test on ubuntu-latest
- Steps:
  1. Checkout code (uses: actions/checkout@v3)
  2. Set up Python 3.11 (uses: actions/setup-python@v4)
  3. Install dependencies from requirements.txt
  4. Run pytest

Return only the YAML content."""
        
        print("Generating ci.yml...")
        ci_yaml = get_completion(ci_prompt, client, model_name, api_provider)
        ci_clean = clean_llm_output(ci_yaml, 'yaml')
        
        save_artifact(ci_clean, '.github/workflows/ci.yml', overwrite=True)
        print("✅ Saved .github/workflows/ci.yml")
        completed.append("Lab 2 Challenge 3 - GitHub Actions")
    except Exception as e:
        errors.append(f"Lab 2 Challenge 3: {str(e)}")
        print(f"❌ Error: {e}")
    
    # FINAL STEP: Build Docker Image
    print_step(8, "BUILD DOCKER IMAGE")
    try:
        print("Building Docker image...")
        result = subprocess.run(
            ['docker', 'build', '-t', 'onboardpro:latest', '.'],
            cwd='c:/Workspace/AG-AISOFTDEV',
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Docker image built successfully")
            completed.append("Docker Build")
        else:
            print(f"⚠️  Docker build failed (exit code {result.returncode})")
            print("STDERR:", result.stderr[:500])
            
            # Retry once
            print("Retrying Docker build...")
            result = subprocess.run(
                ['docker', 'build', '-t', 'onboardpro:latest', '.'],
                cwd='c:/Workspace/AG-AISOFTDEV',
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("✅ Docker build succeeded on retry")
                completed.append("Docker Build (retry)")
            else:
                errors.append(f"Docker Build: failed after retry")
                print("❌ Docker build still failing")
    except Exception as e:
        errors.append(f"Docker Build: {str(e)}")
        print(f"❌ Error: {e}")
    
    # FINAL STEP: Git Commit and Push
    print_step(9, "GIT COMMIT AND PUSH")
    try:
        files_to_commit = [
            'tests/test_main_simple.py',
            'tests/conftest.py',
            'tests/test_main_with_fixture.py',
            'requirements.txt',
            'Dockerfile',
            '.github/workflows/ci.yml'
        ]
        
        # Stage files
        for file in files_to_commit:
            if Path(f'c:/Workspace/AG-AISOFTDEV/{file}').exists():
                subprocess.run(['git', 'add', file], cwd='c:/Workspace/AG-AISOFTDEV')
                print(f"✓ Staged {file}")
        
        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', 'chore: complete Day 4 labs - automated testing and CI/CD pipeline'],
            cwd='c:/Workspace/AG-AISOFTDEV',
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Committed changes")
            
            # Push
            result = subprocess.run(
                ['git', 'push', 'origin', 'main'],
                cwd='c:/Workspace/AG-AISOFTDEV',
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Pushed to main branch")
                completed.append("Git Commit & Push")
            else:
                errors.append(f"Git Push: {result.stderr}")
                print(f"❌ Push failed: {result.stderr[:200]}")
        else:
            print(f"⚠️  Nothing to commit or commit failed: {result.stderr[:200]}")
            
    except Exception as e:
        errors.append(f"Git operations: {str(e)}")
        print(f"❌ Error: {e}")
    
    # FINAL REPORT
    print_step(10, "FINAL SUMMARY REPORT")
    print("\n✅ SUCCESSFULLY COMPLETED STEPS:")
    for item in completed:
        print(f"  ✓ {item}")
    
    if errors:
        print("\n❌ FAILED STEPS:")
        for error in errors:
            print(f"  ✗ {error}")
    
    print("\n📁 FILES CREATED/MODIFIED:")
    for file in files_to_commit:
        path = Path(f'c:/Workspace/AG-AISOFTDEV/{file}')
        if path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (not found)")
    
    print(f"\n🚀 Docker Build: {'SUCCESS' if 'Docker Build' in str(completed) else 'FAILED'}")
    print(f"📤 Git Push: {'SUCCESS' if 'Git Commit & Push' in str(completed) else 'FAILED'}")
    
    print("\n" + "="*70)
    print("EXECUTION COMPLETE")
    print("="*70)

if __name__ == '__main__':
    main()
