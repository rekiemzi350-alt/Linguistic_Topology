import os
import sys
import warnings
import math
from pathlib import Path
from typing import Union, Iterable, List, Optional

# --- Dependency Handling ---
# We try to import torch, but provide a fallback/warning if missing.
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    # Placeholder for type hinting if torch is missing
    class MockTorch:
        Tensor = "torch.Tensor"
    torch = MockTorch()

# We try to import G2P libraries, but will likely fail in a basic env.
# The G2PTokenizer will check availability at runtime.

# --- GELU Activation Functions ---

def gelu_accurate(x):
    if not TORCH_AVAILABLE:
        raise ImportError("PyTorch is required for gelu_accurate")
    if not hasattr(gelu_accurate, "_a"):
        gelu_accurate._a = math.sqrt(2 / math.pi)
    return (
        0.5 * x * (1 + torch.tanh(gelu_accurate._a * (x + 0.044715 * torch.pow(x, 3))))
    )

def gelu(x):
    if not TORCH_AVAILABLE:
        raise ImportError("PyTorch is required for gelu")
    return torch.nn.functional.gelu(x.float()).type_as(x)

# --- Tokenizer Classes ---

class AbsTokenizer:
    """Abstract Base Class for Tokenizers."""
    def __init__(self, **kwargs):
        pass

    def text2tokens(self, line: str) -> List[str]:
        raise NotImplementedError

    def tokens2text(self, tokens: Iterable[str]) -> str:
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}()"

class CharTokenizer(AbsTokenizer):
    def __init__(
        self,
        non_linguistic_symbols: Union[Path, str, Iterable[str]] = None,
        space_symbol: str = "<space>",
        remove_non_linguistic_symbols: bool = False,
        split_with_space: bool = False,
        seg_dict: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.space_symbol = space_symbol
        if non_linguistic_symbols is None:
            self.non_linguistic_symbols = set()
        elif isinstance(non_linguistic_symbols, (Path, str)):
            non_linguistic_symbols = Path(non_linguistic_symbols)
            try:
                with non_linguistic_symbols.open("r", encoding="utf-8") as f:
                    self.non_linguistic_symbols = set(line.rstrip() for line in f)
            except FileNotFoundError:
                warnings.warn(f"{non_linguistic_symbols} doesn't exist.")
                self.non_linguistic_symbols = set()
        else:
            self.non_linguistic_symbols = set(non_linguistic_symbols)
        self.remove_non_linguistic_symbols = remove_non_linguistic_symbols
        self.split_with_space = split_with_space
        self.seg_dict = None
        
        # Placeholder for load_seg_dict which was not provided in snippets
        if seg_dict is not None:
            # self.seg_dict = load_seg_dict(seg_dict)
            warnings.warn("load_seg_dict is not implemented. seg_dict ignored.")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f'space_symbol="{self.space_symbol}"'
            f'non_linguistic_symbols="{self.non_linguistic_symbols}"'
            f")"
        )

    def text2tokens(self, line: Union[str, list]) -> List[str]:
        # Placeholder for seg_tokenize which was not provided
        if self.seg_dict is not None:
            tokens = line.strip().split(" ")
            # tokens = seg_tokenize(tokens, self.seg_dict)
            return tokens
        else:
            tokens = []
            while len(line) != 0:
                for w in self.non_linguistic_symbols:
                    if line.startswith(w):
                        if not self.remove_non_linguistic_symbols:
                            tokens.append(line[: len(w)])
                        line = line[len(w) :]
                        break
                else:
                    t = line[0]
                    if t == " ":
                        # t = "<space>"
                        line = line[1:]
                        continue
                    tokens.append(t)
                    line = line[1:]
        return tokens

    def tokens2text(self, tokens: Iterable[str]) -> str:
        tokens = [t if t != self.space_symbol else " " for t in tokens]
        return "".join(tokens)

class WordTokenizer(AbsTokenizer):
    def __init__(
        self,
        delimiter: str = None,
        non_linguistic_symbols: Union[Path, str, Iterable[str]] = None,
        remove_non_linguistic_symbols: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.delimiter = delimiter

        if not remove_non_linguistic_symbols and non_linguistic_symbols is not None:
            warnings.warn(
                "non_linguistic_symbols is only used "
                "when remove_non_linguistic_symbols = True"
            )

        if non_linguistic_symbols is None:
            self.non_linguistic_symbols = set()
        elif isinstance(non_linguistic_symbols, (Path, str)):
            non_linguistic_symbols = Path(non_linguistic_symbols)
            try:
                with non_linguistic_symbols.open("r", encoding="utf-8") as f:
                    self.non_linguistic_symbols = set(line.rstrip() for line in f)
            except FileNotFoundError:
                warnings.warn(f"{non_linguistic_symbols} doesn't exist.")
                self.non_linguistic_symbols = set()
        else:
            self.non_linguistic_symbols = set(non_linguistic_symbols)
        self.remove_non_linguistic_symbols = remove_non_linguistic_symbols

    def __repr__(self):
        return f'{self.__class__.__name__}(delimiter="{self.delimiter}")'

    def text2tokens(self, line: str) -> List[str]:
        tokens = []
        # Handle split with None (default whitespace) vs specific delimiter
        parts = line.split(self.delimiter) if self.delimiter else line.split()
        for t in parts:
            if self.remove_non_linguistic_symbols and t in self.non_linguistic_symbols:
                continue
            tokens.append(t)
        return tokens

    def tokens2text(self, tokens: Iterable[str]) -> str:
        if self.delimiter is None:
            delimiter = " "
        else:
            delimiter = self.delimiter
        return delimiter.join(tokens)

class G2PTokenizer(AbsTokenizer):
    def __init__(
        self,
        g2p_type: Union[None, str],
        non_linguistic_symbols: Union[Path, str, Iterable[str]] = None,
        space_symbol: str = "<space>",
        remove_non_linguistic_symbols: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # --- G2P Initialization Logic ---
        # Note: This relies on external libraries (g2p_en, pyopenjtalk, phonemizer, etc.)
        # which may not be installed. We will attempt to import them only if requested.
        
        self.g2p = None
        
        if g2p_type is None:
            self.g2p = lambda x: x.split(" ") # Fallback
        elif g2p_type == "g2p_en":
            from g2p_en import G2p as G2p_en
            self.g2p = G2p_en(no_space=False)
        elif g2p_type == "g2p_en_no_space":
            from g2p_en import G2p as G2p_en
            self.g2p = G2p_en(no_space=True)
        elif "pyopenjtalk" in g2p_type:
            import pyopenjtalk
            # Mapping pyopenjtalk functions based on type string
            # Simplified for integration:
            if g2p_type == "pyopenjtalk":
                self.g2p = pyopenjtalk.g2p
            # ... other variants would map to specific wrappers ...
        elif "espeak" in g2p_type:
            from phonemizer.phonemize import phonemize
            # Wrapper for phonemizer
            lang_map = {
                "espeak_ng_arabic": "ar", "espeak_ng_german": "de",
                "espeak_ng_french": "fr-fr", "espeak_ng_spanish": "es",
                "espeak_ng_russian": "ru", "espeak_ng_greek": "el",
                "espeak_ng_english_us_vits": "en-us"
            }
            lang = lang_map.get(g2p_type, "en-us")
            self.g2p = lambda text: phonemize(text, language=lang, backend='espeak', strip=True, with_stress=True).split()
        elif "korean" in g2p_type:
             # from jaso import Jaso ...
             raise NotImplementedError("Korean Jaso G2P not installed.")
        else:
             # Pypinyin etc.
             raise NotImplementedError(f"G2P Type {g2p_type} not fully integrated in this environment.")

        self.g2p_type = g2p_type
        self.space_symbol = space_symbol
        if non_linguistic_symbols is None:
            self.non_linguistic_symbols = set()
        elif isinstance(non_linguistic_symbols, (Path, str)):
            non_linguistic_symbols = Path(non_linguistic_symbols)
            try:
                with non_linguistic_symbols.open("r", encoding="utf-8") as f:
                    self.non_linguistic_symbols = set(line.rstrip() for line in f)
            except FileNotFoundError:
                warnings.warn(f"{non_linguistic_symbols} doesn't exist.")
                self.non_linguistic_symbols = set()
        else:
            self.non_linguistic_symbols = set(non_linguistic_symbols)
        self.remove_non_linguistic_symbols = remove_non_linguistic_symbols

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f'space_symbol="{self.space_symbol}"'
            f'non_linguistic_symbols="{self.non_linguistic_symbols}"'
            f")"
        )

    def text2tokens(self, line: str) -> List[str]:
        tokens = []
        while len(line) != 0:
            for w in self.non_linguistic_symbols:
                if line.startswith(w):
                    if not self.remove_non_linguistic_symbols:
                        tokens.append(line[: len(w)])
                    line = line[len(w) :]
                    break
            else:
                t = line[0]
                tokens.append(t)
                line = line[1:]

        # Reconstruct filtered line
        line = "".join(tokens)
        
        # Apply G2P
        if self.g2p:
            # G2P functions might return list or str, assume list or convert
            g2p_out = self.g2p(line)
            if isinstance(g2p_out, str):
                return g2p_out.split()
            return g2p_out
        return list(line)
