import os
import shutil
from huggingface_hub import snapshot_download

# =============================================================================
# Configuration
#

REPO_ID = "avaktrahu/dataset"

# The local path where the dataset content will be downloaded
# If the directory doesn't exist, it will be created.
DOWNLOAD_PATH = "dataset"

# =============================================================================
# Main
#

def pull_dataset_from_hub():
    """
    Pulls dataset content from the Hugging Face Hub dataset repository to a
    specified local directory.
    """
    print(f"Attempting to pull dataset from repository: {REPO_ID}")
    print(f"Downloading to local path: {DOWNLOAD_PATH}")

    try:
        # Download the snapshot of the repository.
        # This function handles Git LFS and ensures all files are downloaded.
        # 'repo_type="dataset"' specifies that we are dealing with a dataset repository.
        # 'local_dir' is the target directory for the download.
        snapshot_download(
            repo_id=REPO_ID,
            repo_type="dataset",
            local_dir=DOWNLOAD_PATH,
            # For private repositories, ensure you are logged in
            # For public repositories, this is not strictly necessary but good practice
        )
        print("Dataset successfully pulled from the Hugging Face Hub!")
        print(f"Dataset content is available at: {os.path.abspath(DOWNLOAD_PATH)}")

    except Exception as e:
        print(f"Error pulling dataset: {e}")
        print("Please ensure you are logged in and have access to the repository.")
        print("If it's a private repository, ensure your token has read access.")

    finally:
        cleanup()


def cleanup():
    """
    Remove the local cache for this specific repo
    """
    print("\nStarting cache cleanup...")
    try:
        # HF creates a cache directory .cache/huggingface inside download path.
        cache_dir = os.path.join(DOWNLOAD_PATH, ".cache")
        if os.path.exists(cache_dir):
            print(f"Found cache directory: {cache_dir}. Removing...")
            shutil.rmtree(cache_dir)
            print("Cache directory has been successfully removed.")
        else:
            print(f"No cache directory found at: {cache_dir}. No cleanup needed.")

        # And a .gitattributes file
        git_attributes_path = os.path.join(DOWNLOAD_PATH, ".gitattributes")
        if os.path.exists(git_attributes_path):
            print(f"Found .gitattributes file: {git_attributes_path}. Removing...")
            os.remove(git_attributes_path)
            print(".gitattributes file has been successfully removed.")
        else:
            print(f"No .gitattributes file found at: {git_attributes_path}. No cleanup needed.")

    except Exception as e:
        print(f"An error occurred during cache cleanup: {e}")

if __name__ == "__main__":
    # Ensure you are logged in before running this script if the repository is private
    # For public repositories, you might not strictly need to login, but it's good practice.
    # login()  # This will prompt for your Hugging Face token if not already logged in
    pull_dataset_from_hub()
