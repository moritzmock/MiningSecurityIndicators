import re
from argparse import ArgumentParser, \
    ArgumentTypeError
import os
from tqdm import tqdm

def get_mat():
    return ["hack", "todo", "fixme", "xxx"]

def get_SecI():
    return ["access control", "access-control", "access role", "access-role", "adware", "adversarial", "malware",
            "spyware",
            "ransomware", "aes", "antivirus", "anti-virus", "asset", "audit", "authority", "authorise", "availability",
            "bitlocker", "biometric", "blacklist", "black list", "botnet", "buffer overflow", "buffer-overflow", "burp",
            "ctf", "capture the flag", "capture-the-flag", "cbc", "certificate", "checksum", "cipher", "clearance",
            "confidential",
            "clickfraud", "click fraud", "click-fraud", "clickjacking", "click jacking", "click-jacking", "cloudflare",
            "cookie",
            "crc", "credential", "crypt", "csrf", "ddos", "danger", "data exfiltrate", "data-exfiltrate",
            "data exfiltration",
            "data-exfiltration", "data breach", "data-breach", "decode", "defence", "defense", "defensive programming",
            "delegation", "denial of service", "diffie hellman", "directory traversal", "disclose", "disclosure", "dmz",
            "dotfuscator", "dsa", "ecdsa", "encode", "encrypt", "escrow", "exploit", "eviltwin", "evil twin",
            "fingerprint",
            "firewall", "forge", "forgery", "fuzz", "fraud", "gnupg", "gss api", "hack", "hash", "hijacking", "hmac",
            "honeypot",
            "honey pot", "hsm", "inject", "insecure", "integrity", "intrusion", "intruder", "ipsec", "kerberos", "ldap",
            "login",
            "metasploit", "meterpreter", "malicious", "md5", "nessus", "nonce", "nss", "oauth", "obfuscate", "openssl",
            "openssh",
            "openvas", "open auth", "open redirect", "openid", "owasp", "password", "pbkdf2", "pci dss", "pgp",
            "phishing", "pki",
            "privacy", "private key", "privilege", "privilege escalation", "permission escalation", "public key",
            "public-key",
            "pcidss", "pentest", "pen test", "pen-test", "penetration test", "penetration-test", "protect",
            "rainbow table", "rbac",
            "rc4", "repudiation", "rfc 2898", "rijndael", "rootkit", "rsa", "safe", "salt", "saml", "sanitise",
            "sandbox", "scam",
            "scriptkiddie", "script kiddie", "script-kiddie", "scripting", "security", "sftp", "sha", "shellcode",
            "shell code",
            "shell-code", "shibboleth", "shib boleth", "shib-boleth", "signature", "signed", "signing",
            "single sign on",
            "single signon", "single-sign-on", "smart assembly", "smartassembly", "snif", "spam", "spnego", "spoof",
            "ssh", "ssl",
            "sso", "steganography", "tampering", "theft", "threat", "tls", "transport", "tunneling", "tunnelling",
            "trojan", "trust",
            "two factor", "two-factor", "user account", "user-account", "username", "user name", "violate", "validate",
            "virus",
            "whitelist", "white list", "worm", "x 509", "x.509", "xss", "xxe", "ssrf", "zero day", "zero-day", "0 day",
            "0-day",
            "zombie computer", "attack", "vulnerability", "attack vector", "authentication", "cross site", "cross-site",
            "sensitive information", "leak", "information exposure", "path traversal", "use after free", "double free",
            "double-free",
            "man in the middle", "man in middle", "mitm", "poisoning", "unauthorise", "dot dot slash", "bypass",
            "session fixation",
            "forced browsing", "nvd", "cwe", "cve", "capec", "cpe", "common weakness enumeration",
            "common platform enumeration",
            "crack", "xml entity expansion", "http parameter pollution", "eavesdropping", "cryptanalysis", "http flood",
            "http-flood",
            "xml flood", "xml-flood", "udp flood", "udp-flood", "tcp flood", "tcp-flood", "tcp syn flood", "steal",
            "ssl flood",
            "ssl-flood", "j2ee misconfiguration", "asp.net misconfiguration", "improper neutralisation",
            "race condition",
            "null pointer dereference", "untrusted pointer dereference", "trapdoor", "trap door", "backdoor",
            "back door",
            "timebomb", "time bomb", "time-bomb", "xml bomb", "xml-bomb", "logic bomb", "logic-bomb", "captcha",
            "deadlock",
            "missing synchronisation", "incorrect synchronisation", "improper synchronisation", "illegitimate",
            "breach",
            "sql injection", "sql-injection", "unsafe", "un-safe", "failsafe", "fail-safe", "threadsafe", "thread-safe",
            "typesafe",
            "type-safe"]


# taken from https://github.com/melegati/vulsatd-dataset/blob/master/mat.py
# which replicated it from https://github.com/Naplues/MAT/blob/master/src/main/methods/Mat.java
def has_task_words(x, patterns=get_SecI(), index=0):
    words = get_single_words(x)
    for word in words:
        for key in patterns:
            if word.startswith(key) or word.endswith(key):
                if 'xxx' in word and word != 'xxx':
                    return False
                else:
                    return True
    return False


def has_task_words_values(x, patterns=get_SecI(), index=0):
    words = get_single_words(x)
    result = []
    for word in words:
        for key in patterns:
            if word.startswith(key) and word.endswith(key):
                if 'xxx' in word and word != 'xxx':
                    pass
                elif key in result:
                    pass
                else:
                    result.append(key)
                    break
    return result


def get_single_words(x):
    regex = re.compile('[^a-zA-Z\s]')
    regex_space = re.compile('[\s]')
    x_mod = regex.sub("", x)  # replaces non-alpha characters
    x_mod = regex_space.sub(" ", x_mod)  # converts tab and other space characters into a single space
    words = x_mod \
        .lower() \
        .replace("'", "") \
        .split(' ')
    words = [word for word in words if 20 > len(word) > 2]  # removes words which are too short or too long
    return words

def get_multiword_SecI_patterns_value(x, patterns=get_SecI()):
    result = []
    for pattern in patterns:
        if pattern in x:
            result.append(pattern)
    return result


def find_files(root_folder, extension, leave=True):
    results = []
    pbar = tqdm(desc="Finding files in folder...", leave=leave)
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            pbar.update(1)
            if file.endswith(extension):
                results.append(os.path.join(root, file))

    pbar.close()
    return results

def get_comment_regex(pl):
    comment_regex = None
    pl = pl.lower()
    if pl == "go" or pl == "java" or pl == "javascript" or pl == "c" or pl == "cpp":
        comment_regex = re.compile('((\/\*([\s\S]*?)\*\/)|((?<!:)\/\/.*))', re.MULTILINE)
    elif pl == "php":
        comment_regex = re.compile('(((\/\*([\s\S]*?)\*\/)|((?<!:)\/\/.*))|(#.*))', re.MULTILINE)
    elif pl == "ruby":
        comment_regex = re.compile('((#.*)|(\=begin[\s\S]*?\=end))', re.MULTILINE)
    elif pl == "python":
        comment_regex = re.compile('((#.*)|(\'|"){3}[\s\S]*?(\'|"){3})', re.MULTILINE)
    else:
        print("Programming language is not covered... Exiting...")
        quit()

    return comment_regex


def str2bool(v):
    """
    Convert a string representation to a boolean value.
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


def parser():
    args = ArgumentParser()

    args.add_argument('--path', type=str, help='path to repository', required=True)
    args.add_argument('--path_logs', type=str, help='path to repository', required=False, default="logs")
    args.add_argument('--MAT', type=str2bool, default=False)
    args.add_argument('--GITHUB', type=str, default=False)
    args.add_argument('--JIRA_PROJECT', type=str, default=False)

    parsed_args = args.parse_args()

    if not os.path.exists(parsed_args.path_logs):
        os.makedirs(parsed_args.path_logs)

    return parsed_args


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        print(file_path)
        print("File not found.")
    except Exception as e:
        print(file_path)
        print("An error occurred:", e)


def detect_SecI(x):
    global vector
    single_words_SecI = [pattern for pattern in get_SecI() if len(pattern.split(" ")) == 1]
    multi_words_SecI = [pattern for pattern in get_SecI() if len(pattern.split(" ")) != 1]
    vector_single = has_task_words_values(x, patterns=single_words_SecI)
    vector_multiple = get_multiword_SecI_patterns_value(x, patterns=multi_words_SecI)
    return vector_single + vector_multiple