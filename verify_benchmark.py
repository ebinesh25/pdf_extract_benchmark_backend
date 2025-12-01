import requests
import time
import subprocess
import sys
import os

def run_verification():
    # Start the server in the background
    print("Starting server...")
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Define the URL
        url = "http://127.0.0.1:8001/api/v1/benchmark"
        
        # Create a dummy PDF file for testing
        with open("test.pdf", "wb") as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000117 00000 n\n0000000236 00000 n\n0000000323 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n417\n%%EOF")

        # Prepare the request
        files = {'file': ('test.pdf', open('test.pdf', 'rb'), 'application/pdf')}
        params = [('tools', 'pymupdf'), ('tools', 'pypdf')]
        data = {'ground_truth': 'Hello World'}
        
        print(f"Sending request to {url}...")
        response = requests.post(url, files=files, params=params, data=data)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(response.json())
        else:
            print("Error Response:")
            print(response.text)

    except Exception as e:
        print(f"Verification failed: {e}")
    finally:
        # Cleanup
        print("Stopping server...")
        process.terminate()
        if os.path.exists("test.pdf"):
            os.remove("test.pdf")

if __name__ == "__main__":
    run_verification()
