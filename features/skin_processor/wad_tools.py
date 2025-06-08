import subprocess
from pathlib import Path

class WadTools:
    def __init__(self, tools_path, logger):
        self.tools_path = Path(tools_path)
        self.logger = logger
    
    def extract_wads(self, wad_dir):
        wad_extract_exe = self.tools_path / "wad-extract.exe"
        
        self.logger.log(f"wad-extract.exe path: {wad_extract_exe}")
        self.logger.log(f"Exists: {wad_extract_exe.exists()}")
        
        wad_files = list(wad_dir.glob("*.wad.client"))
        self.logger.log(f"WAD files found: {[f.name for f in wad_files]}")
        
        if not wad_files:
            self.logger.log("No .wad.client files found!")
            return
            
        for wad_file in wad_files:
            self.logger.log(f"Extracting {wad_file.name}...")
            self.logger.log(f"File size: {wad_file.stat().st_size} bytes")
            
            wad_extract_abs = Path.cwd() / self.tools_path / "wad-extract.exe"
            wad_file_abs = Path.cwd() / wad_file
            
            cmd = [str(wad_extract_abs), str(wad_file_abs)]
            self.logger.log(f"Command: {' '.join(cmd)}")
            self.logger.log(f"Working directory: {Path.cwd()}")
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path.cwd()), timeout=120)
                
                self.logger.log(f"Return code: {result.returncode}")
                if result.stdout:
                    self.logger.log(f"Output: {result.stdout[:500]}...")
                if result.stderr:
                    self.logger.log(f"Error: {result.stderr}")
                    
                if result.returncode != 0:
                    raise Exception(f"Error extracting {wad_file.name}: Code {result.returncode}, {result.stderr}")
                else:
                    self.logger.log(f"Extraction of {wad_file.name} successful")
                    
            except subprocess.TimeoutExpired:
                self.logger.log(f"Timeout extracting {wad_file.name} (more than 2 minutes)")
                raise Exception(f"Timeout extracting {wad_file.name}")
    
    def convert_dds_files(self, wad_dir):
        tex2dds_exe = self.tools_path / "tex2dds.exe"
        
        self.logger.log(f"tex2dds.exe path: {tex2dds_exe}")
        self.logger.log(f"Exists: {tex2dds_exe.exists()}")
        
        extracted_dirs = [d for d in wad_dir.iterdir() if d.is_dir()]
        self.logger.log(f"Extracted directories found: {[d.name for d in extracted_dirs]}")
        
        for extracted_dir in extracted_dirs:
            self.logger.log(f"=== Analyzing directory {extracted_dir.name} ===")
            
            all_files = list(extracted_dir.rglob("*"))
            self.logger.log(f"All files in {extracted_dir.name}: {len(all_files)}")
            
            file_extensions = {}
            for f in all_files:
                if f.is_file():
                    ext = f.suffix.lower()
                    file_extensions[ext] = file_extensions.get(ext, 0) + 1
            
            self.logger.log(f"Extensions found: {dict(file_extensions)}")
            
            dds_files = list(extracted_dir.rglob("*.dds"))
            self.logger.log(f".dds files in {extracted_dir.name}: {len(dds_files)}")
            
            if dds_files:
                self.logger.log(f"List of .dds files: {[f.name for f in dds_files[:5]]}{'...' if len(dds_files) > 5 else ''}")
            
            for i, dds_file in enumerate(dds_files):
                self.logger.log(f"=== Conversion {i+1}/{len(dds_files)}: {dds_file.name} ===")
                self.logger.log(f"Full path: {dds_file.relative_to(wad_dir)}")
                self.logger.log(f"Size: {dds_file.stat().st_size} bytes")
                
                tex2dds_abs = Path.cwd() / self.tools_path / "tex2dds.exe"
                
                cmd = [str(tex2dds_abs), dds_file.name]
                self.logger.log(f"Command: {' '.join(cmd)}")
                self.logger.log(f"Working directory: {dds_file.parent}")
                self.logger.log(f"File exists: {dds_file.exists()}")
                
                tex_file = dds_file.with_suffix('.tex')
                self.logger.log(f"Corresponding .tex file: {tex_file.name} (exists: {tex_file.exists()})")
                
                try:
                    self.logger.log(f"Starting conversion (timeout: 60s)...")
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(dds_file.parent), timeout=60)
                    
                    self.logger.log(f"Conversion completed - Code: {result.returncode}")
                    
                    if result.stdout:
                        self.logger.log(f"Stdout output: {result.stdout}")
                    if result.stderr:
                        self.logger.log(f"Stderr output: {result.stderr}")
                    
                    if result.returncode != 0:
                        self.logger.log(f"ERROR: Conversion failed for {dds_file.name}")
                    else:
                        if tex_file.exists():
                            self.logger.log(f"SUCCESS: .tex file created ({tex_file.stat().st_size} bytes)")
                        else:
                            self.logger.log(f"WARNING: No .tex file created despite success")
                        
                except subprocess.TimeoutExpired:
                    self.logger.log(f"TIMEOUT: Conversion of {dds_file.name} (more than 60 seconds)")
                    self.logger.log("This may indicate a problem with the tool or file")
                except Exception as e:
                    self.logger.log(f"EXCEPTION: {str(e)}")
            
            if not dds_files:
                self.logger.log(f"No .dds files found in {extracted_dir.name}, moving to next step")
    
    def rebuild_wads(self, wad_dir):
        wad_make_exe = self.tools_path / "wad-make.exe"
        
        self.logger.log(f"wad-make.exe path: {wad_make_exe}")
        self.logger.log(f"Exists: {wad_make_exe.exists()}")
        
        extracted_dirs = [d for d in wad_dir.iterdir() if d.is_dir()]
        self.logger.log(f"Directories to rebuild: {[d.name for d in extracted_dirs]}")
        
        for extracted_dir in extracted_dirs:
            self.logger.log(f"=== Rebuilding {extracted_dir.name} ===")
            
            files_in_dir = list(extracted_dir.rglob("*"))
            self.logger.log(f"Number of files in {extracted_dir.name}: {len([f for f in files_in_dir if f.is_file()])}")
            
            wad_make_abs = Path.cwd() / self.tools_path / "wad-make.exe"
            extracted_dir_abs = Path.cwd() / extracted_dir
            
            cmd = [str(wad_make_abs), str(extracted_dir_abs)]
            self.logger.log(f"Command: {' '.join(cmd)}")
            self.logger.log(f"Working directory: {Path.cwd()}")
            
            try:
                self.logger.log(f"Starting rebuild (timeout: 3 minutes)...")
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path.cwd()), timeout=180)
                
                self.logger.log(f"Return code: {result.returncode}")
                if result.stdout:
                    self.logger.log(f"Output: {result.stdout[:500]}...")
                if result.stderr:
                    self.logger.log(f"Error: {result.stderr}")
                    
                if result.returncode != 0:
                    raise Exception(f"Error rebuilding {extracted_dir.name}: Code {result.returncode}, {result.stderr}")
                else:
                    self.logger.log(f"Rebuild of {extracted_dir.name} successful")
                    
                    new_wad_files = list(wad_dir.glob("*.wad.client"))
                    self.logger.log(f"WAD files after rebuild: {[f.name for f in new_wad_files]}")
                    
            except subprocess.TimeoutExpired:
                self.logger.log(f"Timeout rebuilding {extracted_dir.name} (more than 3 minutes)")
                raise Exception(f"Timeout rebuilding {extracted_dir.name}") 