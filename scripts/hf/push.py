import os
from datetime import datetime, timezone
from huggingface_hub import create_repo, HfApi

# =============================================================================
# Configuration
#

REPO_ID = "avaktrahu/dataset"

DATASET_PATH = "dataset"

# =============================================================================
# Main
#

def push_dataset_to_hub():
    """
    Pushes local dataset content to the Hugging Face Hub dataset repository.
    """
    # Initialize the Hugging Face API client
    api = HfApi()

    # Create a new dataset repository on the Hub
    # The 'exist_ok=True' flag ensures the script doesn't fail if the repo already exists.
    print(f"Creating or checking for repository: {REPO_ID}")
    create_repo(repo_id=REPO_ID, repo_type="dataset", exist_ok=True)
    print(f"Repository {REPO_ID} is ready.")

    # Check if the dataset path exists
    if not os.path.isdir(DATASET_PATH):
        print(f"Error: The local dataset directory '{DATASET_PATH}' does not exist.")
        return

    # Upload all files from the local directory to the repository
    # The 'repo_id' specifies where to upload.
    # The 'folder_path' is the local directory to upload from.
    # The 'commit_message' provides a descriptive commit message.
    print(f"Uploading content from '{DATASET_PATH}' to '{REPO_ID}'...")
    api.upload_folder(
        repo_id=REPO_ID,
        folder_path=DATASET_PATH,
        repo_type="dataset",
        commit_message=f"Update dataset content on {datetime.now(timezone.utc).isoformat()}"
    )
    print("Dataset successfully pushed to the Hugging Face Hub!")
    print(f"You can view your dataset here: https://huggingface.co/datasets/{REPO_ID}")


if __name__ == "__main__":
    # Ensure you are logged in before running this script
    from huggingface_hub import login
    login()  # This will prompt for your Hugging Face token if not already logged in
    push_dataset_to_hub()
