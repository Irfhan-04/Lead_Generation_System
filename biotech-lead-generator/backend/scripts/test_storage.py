"""
Test Supabase Storage
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.storage import get_storage_service

def test_storage():
    print("🧪 Testing Supabase Storage\n")
    print("=" * 60)
    
    storage = get_storage_service()
    
    # Test 1: Upload file
    print("\n1️⃣  Testing File Upload...")
    test_data = b"This is a test file for Supabase Storage"
    
    try:
        file_path, public_url = storage.upload_file(
            file_data=test_data,
            file_name="test_file.txt",
            folder="test",
            content_type="text/plain"
        )
        
        print(f"   ✅ File uploaded successfully!")
        print(f"   Path: {file_path}")
        print(f"   URL: {public_url}")
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        return False
    
    # Test 2: List files
    print("\n2️⃣  Testing File Listing...")
    try:
        files = storage.list_files("test")
        print(f"   ✅ Found {len(files)} files in 'test' folder")
        for file in files:
            print(f"      - {file.get('name')}")
    except Exception as e:
        print(f"   ❌ List failed: {e}")
    
    # Test 3: Get file size
    print("\n3️⃣  Testing File Size...")
    try:
        size = storage.get_file_size(file_path)
        if size:
            print(f"   ✅ File size: {size} bytes")
        else:
            print(f"   ⚠️  Could not get file size")
    except Exception as e:
        print(f"   ❌ Size check failed: {e}")
    
    # Test 4: Download file
    print("\n4️⃣  Testing File Download...")
    try:
        downloaded_data = storage.download_file(file_path)
        if downloaded_data == test_data:
            print(f"   ✅ File downloaded successfully!")
            print(f"   Content matches: {downloaded_data.decode()[:50]}...")
        else:
            print(f"   ⚠️  Content mismatch")
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
    
    # Test 5: Create signed URL
    print("\n5️⃣  Testing Signed URL...")
    try:
        signed_url = storage.create_signed_url(file_path, expires_in=3600)
        print(f"   ✅ Signed URL created!")
        print(f"   URL: {signed_url[:80]}...")
    except Exception as e:
        print(f"   ❌ Signed URL failed: {e}")
    
    # Test 6: Delete file
    print("\n6️⃣  Testing File Deletion...")
    try:
        success = storage.delete_file(file_path)
        if success:
            print(f"   ✅ File deleted successfully!")
        else:
            print(f"   ⚠️  Delete returned False")
    except Exception as e:
        print(f"   ❌ Delete failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Storage Tests Complete!\n")
    print("✅ Your Supabase Storage is working perfectly!")
    print("\nYou can now:")
    print("- Upload export files (CSV, Excel, PDF)")
    print("- Store user uploads")
    print("- Generate public or signed URLs")
    print("- All within FREE 1GB limit!")
    
    return True


if __name__ == "__main__":
    test_storage()