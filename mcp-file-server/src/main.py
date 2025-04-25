from mcp.server.fastmcp import FastMCP
import os
import shutil
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileSystemTools:
    def __init__(self):
        self.home_dir = str(Path.home())
        
    @staticmethod
    def _ensure_path_exists(path):
        """Ensure parent directories exist"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
            
    def create_directory(self, path: str) -> dict:
        """
        Creates a directory at the specified path.
        
        Args:
            path (str): Full path where directory should be created
            
        Returns:
            dict: Success status and message
        """
        try:
            os.makedirs(path, exist_ok=True)
            return {"success": True, "message": f"Created directory: {path}"}
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {str(e)}")
            return {"success": False, "error": str(e)}
                
    def move_file(self, source: str, destination: str) -> dict:
        """
        Moves a file from source to destination.
        
        Args:
            source (str): Source file path
            destination (str): Destination file path
            
        Returns:
            dict: Success status and message
        """
        try:
            self._ensure_path_exists(destination)
            shutil.move(source, destination)
            return {
                "success": True,
                "message": f"Moved {source} to {destination}"
            }
        except Exception as e:
            logger.error(f"Failed to move file from {source} to {destination}: {str(e)}")
            return {"success": False, "error": str(e)}

def main():
    try:
        # Initialize MCP server
        mcp = FastMCP('FileSystemTools')
        logger.info("MCP server initialized")
        
        # Register tools
        fs_tools = FileSystemTools()
        
        @mcp.tool()
        def create_directory(path: str):
            """Creates a directory at the specified path."""
            return fs_tools.create_directory(path)
        
        @mcp.tool()
        def move_file(source: str, destination: str):
            """Moves a file from source to destination."""
            return fs_tools.move_file(source, destination)
        
        logger.info("Starting MCP server...")
        # Run the server
        mcp.run(transport="stdio")
        
    except Exception as e:
        logger.error(f"Failed to start MCP server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
