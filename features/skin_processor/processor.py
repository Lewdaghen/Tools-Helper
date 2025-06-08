import shutil
import threading
import re
from pathlib import Path
from .wad_tools import WadTools
from utils.file_utils import FileManager

class SkinProcessor:
    def __init__(self, config_manager, logger):
        self.config = config_manager
        self.logger = logger
        self.tools_path = self.determine_tools_path()
        self.wad_tools = WadTools(self.tools_path, logger)
        
        self.installed_path = Path(self.config.get_cslol_path()) / "installed"
        self.backup_path = Path(FileManager.generate_unique_dir_name("backup"))
        self.process_path = Path(FileManager.generate_unique_dir_name("process"))
    
    def determine_tools_path(self):
        local_tools = Path("cslol-tools")
        if local_tools.exists() and (local_tools / "wad-extract.exe").exists():
            self.logger.log("Using local CSLoL tools")
            return local_tools
        
        cslol_path = Path(self.config.get_cslol_path())
        if cslol_path.exists():
            cslol_tools = cslol_path / "cslol-tools"
            if cslol_tools.exists() and (cslol_tools / "wad-extract.exe").exists():
                self.logger.log("Using CSLoL Manager tools")
                return cslol_tools
        
        self.logger.log("WARNING: No CSLoL tools found")
        return local_tools
    
    def get_available_skins(self):
        if not self.installed_path.exists():
            return []
        return [d.name for d in self.installed_path.iterdir() if d.is_dir()]
    
    def get_skins_by_champion(self):
        skins = self.get_available_skins()
        champion_skins = {}
        
        champion_emojis = {
            'aatrox': '⚔️',
            'ahri': '🦊',
            'akali': '🥷',
            'alistar': '🐂',
            'ammu': '🧻',
            'anivia': '🐦‍🔥',
            'annie': '🔥',
            'aphelios': '🌙',
            'ashe': '🏹',
            'azir': '🏛️',
            'bard': '🎵',
            'blitzcrank': '🤖',
            'braum': '🛡️',
            'caitlyn': '🔫',
            'camille': '⚔️',
            'cassiopeia': '🐍',
            'chogath': '👹',
            'corki': '✈️',
            'darius': '🪓',
            'diana': '🌙',
            'draven': '🪓',
            'ekko': '⏰',
            'elise': '🕷️',
            'evelynn': '😈',
            'ezreal': '✨',
            'fiddlesticks': '🎃',
            'fiora': '⚔️',
            'fizz': '🐟',
            'galio': '🗿',
            'gangplank': '🏴‍☠️',
            'garen': '⚔️',
            'gnar': '🦕',
            'graves': '🔫',
            'gwen': '✂️',
            'hecarim': '🐎',
            'heimerdinger': '🔧',
            'illaoi': '🐙',
            'irelia': '⚔️',
            'ivern': '🌳',
            'janna': '💨',
            'jarvaniv': '👑',
            'jax': '🔨',
            'jayce': '⚡',
            'jhin': '🎭',
            'jinx': '💣',
            'kaisa': '🦋',
            'kalista': '👻',
            'karma': '☯️',
            'karthus': '💀',
            'kassadin': '💫',
            'katarina': '🗡️',
            'kayle': '😇',
            'kayn': '😈',
            'kennen': '⚡',
            'khazix': '🦗',
            'kindred': '🐺',
            'kled': '🦎',
            'kogmaw': '👾',
            'leblanc': '✨',
            'leesin': '👊',
            'leona': '☀️',
            'lillia': '🦌',
            'lissandra': '❄️',
            'lucian': '🔫',
            'lulu': '🧚',
            'lux': '💡',
            'malphite': '🗿',
            'malzahar': '👁️',
            'maokai': '🌳',
            'masteryi': '⚔️',
            'milio': '🔥',
            'missfortune': '🏴‍☠️',
            'mordekaiser': '💀',
            'morgana': '😈',
            'nami': '🌊',
            'nasus': '🐕',
            'nautilus': '⚓',
            'neeko': '🦎',
            'nidalee': '🐆',
            'nocturne': '😴',
            'nunu': '⛄',
            'olaf': '🪓',
            'orianna': '🤖',
            'ornn': '🔨',
            'pantheon': '🛡️',
            'poppy': '🔨',
            'pyke': '🗡️',
            'qiyana': '💎',
            'quinn': '🦅',
            'rakan': '🕊️',
            'rammus': '🔄',
            'reksai': '🐛',
            'rell': '⚔️',
            'renata': '🧪',
            'renekton': '🐊',
            'rengar': '🦁',
            'riven': '⚔️',
            'rumble': '🤖',
            'ryze': '📜',
            'samira': '🔫',
            'sejuani': '🐗',
            'senna': '💀',
            'seraphine': '🎤',
            'sett': '👊',
            'shaco': '🃏',
            'shen': '🥷',
            'shyvana': '🐉',
            'singed': '☣️',
            'sion': '💀',
            'sivir': '🪃',
            'skarner': '🦂',
            'sona': '🎼',
            'soraka': '⭐',
            'swain': '🐦‍⬛',
            'sylas': '⛓️',
            'syndra': '🔮',
            'tahmkench': '🐸',
            'taliyah': '🪨',
            'talon': '🗡️',
            'taric': '💎',
            'teemo': '🍄',
            'thresh': '⛓️',
            'tristana': '💥',
            'trundle': '🧌',
            'tryndamere': '⚔️',
            'twistedfate': '🃏',
            'twitch': '🐀',
            'udyr': '🐻',
            'urgot': '🦀',
            'varus': '🏹',
            'vayne': '🔫',
            'veigar': '🎩',
            'velkoz': '👁️',
            'vex': '😭',
            'vi': '👊',
            'viego': '👑',
            'viktor': '🤖',
            'vladimir': '🩸',
            'volibear': '🐻',
            'warwick': '🐺',
            'wukong': '🐵',
            'xayah': '🪶',
            'xerath': '⚡',
            'xinzhao': '🗡️',
            'yasuo': '🌪️',
            'yone': '👻',
            'yorick': '⚰️',
            'yuumi': '🐱',
            'zac': '🟢',
            'zed': '🥷',
            'zeri': '⚡',
            'ziggs': '💣',
            'zilean': '⏰',
            'zoe': '⭐',
            'zyra': '🌹'
        }
        
        for skin in skins:
            champion_name = self.extract_champion_from_wad(skin)
            if champion_name:
                if champion_name not in champion_skins:
                    emoji = champion_emojis.get(champion_name.lower(), '🎨')
                    champion_skins[champion_name] = {
                        'emoji': emoji,
                        'skins': []
                    }
                champion_skins[champion_name]['skins'].append(skin)
        
        for champion_data in champion_skins.values():
            champion_data['skins'].sort()
        
        return champion_skins
    
    def extract_champion_from_wad(self, skin_name):
        skin_path = self.installed_path / skin_name
        wad_path = skin_path / "WAD"
        
        self.logger.log(f"🔍 Analyzing skin: {skin_name}")
        self.logger.log(f"   WAD path: {wad_path}")
        self.logger.log(f"   WAD exists: {wad_path.exists()}")
        
        if not wad_path.exists():
            self.logger.log(f"   ⚠️ No WAD directory found for {skin_name}")
            return self.extract_champion_name_fallback(skin_name)
        
        wad_files = list(wad_path.glob("*.wad.client"))
        self.logger.log(f"   WAD files found: {[f.name for f in wad_files]}")
        
        if not wad_files:
            self.logger.log(f"   ⚠️ No .wad.client files found for {skin_name}")
            return self.extract_champion_name_fallback(skin_name)
        
        wad_file = wad_files[0]
        champion_name = wad_file.stem.replace('.wad', '')
        
        self.logger.log(f"   ✅ Champion extracted: {champion_name}")
        
        return champion_name.title()
    
    def extract_champion_name_fallback(self, skin_name):
        skin_lower = skin_name.lower()
        
        patterns = [
            r'^([a-z]+)_?(?:skin|mod|custom)',
            r'^([a-z]+)_.*',
            r'^([a-z]+)\d+',
            r'^([a-z]+)[_\-\s]',
            r'^([a-z]+)'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, skin_lower)
            if match:
                champion = match.group(1)
                if len(champion) >= 3:
                    return champion.title()
        
        if '_' in skin_lower:
            parts = skin_lower.split('_')
            if len(parts[0]) >= 3:
                return parts[0].title()
        
        if len(skin_lower) >= 3:
            return skin_lower[:10].title()
        
        return "Unknown"
    
    def setup_directories(self):
        FileManager.cleanup_old_work_directories(Path.cwd(), ["process_*", "backup_*"], self.logger)
        
        for directory in [self.backup_path, self.process_path]:
            if directory.exists():
                self.logger.log(f"⚠ Directory {directory.name} already exists, removing...")
                FileManager.force_remove_directory(directory, self.logger)
            directory.mkdir(exist_ok=True)
            
        self.logger.log(f"Directories {self.backup_path.name} and {self.process_path.name} created")
    
    def process_skins(self, selected_skins, progress_callback=None):
        try:
            self.logger.log(f"Starting processing of {len(selected_skins)} skins...")
            self.setup_directories()
            
            for i, skin in enumerate(selected_skins):
                if progress_callback:
                    progress_callback(f"Processing: {skin} ({i+1}/{len(selected_skins)})")
                self.process_single_skin(skin)
                
            self.logger.log("Processing completed successfully!")
            return True
            
        except Exception as e:
            self.logger.log(f"Error: {str(e)}")
            raise
    
    def process_single_skin(self, skin_name):
        skin_path = self.installed_path / skin_name
        backup_skin_path = self.backup_path / skin_name
        process_skin_path = self.process_path / skin_name
        
        self.logger.log(f"=== Processing {skin_name} ===")
        self.logger.log(f"Source path: {skin_path}")
        self.logger.log(f"Exists: {skin_path.exists()}")
        
        if not skin_path.exists():
            self.logger.log(f"ERROR: Skin {skin_name} does not exist!")
            return
        
        self.logger.log(f"Backing up {skin_name}...")
        shutil.copytree(skin_path, backup_skin_path)
        
        self.logger.log(f"Copying {skin_name} to process...")
        shutil.copytree(skin_path, process_skin_path)
        
        wad_dir = process_skin_path / "WAD"
        self.logger.log(f"Looking for WAD directory: {wad_dir}")
        self.logger.log(f"WAD directory exists: {wad_dir.exists()}")
        
        if not wad_dir.exists():
            self.logger.log(f"No WAD directory for {skin_name}, skipping")
            return
            
        self.logger.log(f"Extracting WADs for {skin_name}...")
        self.wad_tools.extract_wads(wad_dir)
        
        self.logger.log(f"Converting .dds files for {skin_name}...")
        self.wad_tools.convert_dds_files(wad_dir)
        
        self.logger.log(f"Rebuilding WADs for {skin_name}...")
        self.wad_tools.rebuild_wads(wad_dir)
        
        self.logger.log(f"Replacing {skin_name} in installed...")
        if skin_path.exists():
            shutil.rmtree(skin_path)
        shutil.copytree(process_skin_path, skin_path)
        
        self.logger.log(f"✅ {skin_name} processed successfully") 