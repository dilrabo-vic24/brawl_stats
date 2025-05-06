import gzip
import zlib
import brotli
from typing import Union, List, Optional 

def decompress_content(raw_content: bytes, content_encoding: str) -> Optional[bytes]: 
    """
    Decompresses raw byte content based on the provided content_encoding.
    ... (qolgan docstring) ...
    """
    encoding = content_encoding.lower()
    decompressed_bytes = None

    if 'gzip' in encoding:
        print("Attempting gzip decompression...")
        try:
            decompressed_bytes = gzip.decompress(raw_content)
            print("Gzip decompression successful.")
        except gzip.BadGzipFile as e_gz_bad:
            print(f"BadGzipFile error: {e_gz_bad}. Content might not be gzipped or is corrupted.")
            return raw_content 
        except Exception as e_gz:
            print(f"Error decompressing gzip: {e_gz}")
            return None
    
    elif 'deflate' in encoding:
        print("Attempting deflate decompression...")
        try:
            decompressed_bytes = zlib.decompress(raw_content, -zlib.MAX_WBITS)
            print("Raw deflate decompression successful.")
        except zlib.error:
            try:
                decompressed_bytes = zlib.decompress(raw_content)
                print("Standard zlib (with header) decompression successful.")
            except Exception as e_df:
                print(f"Error decompressing deflate with zlib header: {e_df}")
                return None
        except Exception as e_df_other:
             print(f"Other error during deflate decompression: {e_df_other}")
             return None

    elif 'br' in encoding:
        print("Attempting brotli decompression...")
        try:
            if brotli:
                decompressed_bytes = brotli.decompress(raw_content)
                print("Brotli decompression successful.")
            else:
                print("Brotli library not installed. Cannot decompress 'br' content.")
                return raw_content
        except Exception as e_br:
            print(f"Error decompressing brotli: {e_br}")
            return None
    
    if decompressed_bytes is not None:
        return decompressed_bytes
    else:
        print(f"No known compression ('{encoding}') or decompression was skipped, returning raw content.")
        return raw_content

def decode_bytes_to_string(
    content_bytes: bytes, 
    detected_encoding: Optional[str] = None,  
    fallback_encodings: List[str] = ['utf-8', 'iso-8859-1', 'windows-1251']
) -> Optional[str]: 
    """
    Decodes a byte string into a Python string using a list of potential encodings.
    ... (qolgan docstring) ...
    """
    if not content_bytes:
        return None

    encodings_to_attempt = []
    if detected_encoding:
        encodings_to_attempt.append(detected_encoding.lower())
    
    for fe in fallback_encodings:
        if fe.lower() not in encodings_to_attempt:
            encodings_to_attempt.append(fe.lower())
    
    for encoding_H in encodings_to_attempt:
        try:
            print(f"Attempting to decode with: {encoding_H}")
            decoded_string = content_bytes.decode(encoding_H)
            print(f"Successfully decoded with {encoding_H}.")
            return decoded_string
        except UnicodeDecodeError:
            print(f"Failed to decode with {encoding_H} (UnicodeDecodeError).")
        except Exception as e:
            print(f"Error decoding with {encoding_H}: {e}")
    
    print("Could not decode content with any of the provided encodings.")
    return None