from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from typing import NamedTuple


class BadFile(NamedTuple):
    filename: str
    key: str
    pattern_name: str


# Patterns based on https://github.com/gitleaks/gitleaks/pull/1291
# Azure Data Factory SHIR Key format: IR@{GUID}@{resource_name}@{location}@{base64}
AZURE_DATAFACTORY_SHIR_PATTERN = re.compile(
    rb"IR@[0-9a-zA-Z-]{36}@[^@\s]+@[0-9a-zA-Z\-=]*@[A-Za-z0-9+/=]{44}",
)

# CSCAN0020, CSCAN0030 - App service deployment secrets
AZURE_APP_SERVICE_DEPLOYMENT_PATTERN = re.compile(
    rb"MII[a-zA-Z0-9=_\-]{200,}",
)

# CSCAN0030, CSCAN0090, CSCAN0150 - Storage credentials (86 char)
AZURE_STORAGE_86CHAR_PATTERN = re.compile(
    rb"[ \t]{0,10}[a-zA-Z0-9/+]{86}==",
)

# CSCAN0030, CSCAN0090, CSCAN0150 - Storage credentials (43 char)
AZURE_STORAGE_43CHAR_PATTERN = re.compile(
    rb"[a-zA-Z0-9/+]{43}=[^{@\d%\s]",
)

# CSCAN0030, CSCAN0090, CSCAN0150 - SAS/sig tokens
AZURE_STORAGE_SIG_PATTERN = re.compile(
    rb"(?:sig|sas|password)=[a-zA-Z0-9%]{43,53}%3[dD]",
    re.IGNORECASE,
)

# CSCAN0030 - Storage credential with userid/password
AZURE_STORAGE_USERIDPW_PATTERN = re.compile(
    rb'(?:user ?(?:id|name)|uid)=.{2,128}?\s*;\s*(?:password|pwd)=[^\'\$%>@\'";\[{][^;"\']{2,350}?[;"\']',
    re.IGNORECASE,
)

# CSCAN0030 - AccountKey with MII prefix
AZURE_STORAGE_ACCOUNTKEY_PATTERN = re.compile(
    rb"AccountKey\s*=\s*MII[a-zA-Z0-9/+]{43,}={0,2}",
    re.IGNORECASE,
)

# CSCAN0100 - Service Bus SharedAccessKey
AZURE_STORAGE_SERVICEBUS_PATTERN = re.compile(
    rb'<ServiceBusAccountInfo.*?SharedAccessKey\s*=\s*["\'][a-zA-Z0-9/+]{10,}["\']',
    re.IGNORECASE | re.DOTALL,
)

# CSCAN0130 - Monitoring Agent credentials
AZURE_STORAGE_MONIKER_PATTERN = re.compile(
    rb"Account Moniker\s*=.*?key\s*=",
    re.IGNORECASE,
)

# CSCAN0110 - Blob URL with SAS token
AZURE_STORAGE_BLOBURL_PATTERN = re.compile(
    rb"https://[a-zA-Z0-9-]+\.(?:blob|file|queue|table|dfs|z\d+\.web)\.core\.windows\.net/.*?sig=[a-zA-Z0-9%]{30,}",
    re.IGNORECASE,
)

# CSCAN0090 - decryptionKey/validationKey
AZURE_PASSWORD_MACHINEKEY_PATTERN = re.compile(
    rb'(?:decryptionKey|validationKey)\s*=\s*["\'][^"\']+["\']',
    re.IGNORECASE,
)

# CSCAN0090 - <add> elements with keys/secrets
AZURE_PASSWORD_ADDKEY_PATTERN = re.compile(
    rb'<add\s+.*?(?:key(?:s|\d)?|credentials?|secrets?(?:S|\d)?|(?:password|token|key)(?:primary|secondary|orsas|sas|encrypted))\s*=\s*["\'][^"\']+["\'].*?value\s*=\s*["\'][^"\']+["\']',
    re.IGNORECASE,
)

# CSCAN0090 - Connection strings with password
AZURE_PASSWORD_CONNSTRING_PATTERN = re.compile(
    rb'(?:connectionstring|connstring)[^=]*?=["\'][^"\']*?password=[^\$\s;][^"\'\s]*?[;"\']',
    re.IGNORECASE,
)

# CSCAN0090 - Base64 values
AZURE_PASSWORD_VALUE_PATTERN = re.compile(
    rb'value\s*=\s*["\'](?:[A-Za-z0-9+/]{4}){1,200}==["\']',
    re.IGNORECASE,
)

# CSCAN0090, CSCAN0150 - uid/password pairs
AZURE_PASSWORD_UIDPW_PATTERN = re.compile(
    rb'(?:user ?(?:id|name)|uid)=.{2,128}?\s*;\s*(?:password|pwd)=[^\'\$%@\'";\[{][^;"\']{2,350}?[;"\']',
    re.IGNORECASE,
)

# CSCAN0160 - NetworkCredential with domain
AZURE_NETWORK_CREDENTIAL_PATTERN = re.compile(
    rb"NetworkCredential\([^)]*?(?:corp|europe|middleeast|northamerica|southpacific|southamerica|fareast|africa|redmond|exchange|extranet|partners|extranettest|parttest|noe|ntdev|ntwksta|sys-wingroup|windeploy|wingroup|winse|segroup|xcorp|xrep|phx|gme|usme|cdocidm|mslpa)\)",
    re.IGNORECASE,
)

# CSCAN0160 - schtasks with domain credentials
AZURE_NETWORK_SCHTASKS_PATTERN = re.compile(
    rb"schtasks.*?/ru\s+(?:corp|europe|middleeast|northamerica|southpacific|southamerica|fareast|africa|redmond|exchange|extranet|partners|extranettest|parttest|noe|ntdev|ntwksta|sys-wingroup|windeploy|wingroup|winse|segroup|xcorp|xrep|phx|gme|usme|cdocidm|mslpa).*?/rp",
    re.IGNORECASE,
)

# CSCAN0160 - .NET NetworkCredential
AZURE_NETWORK_DOTNET_PATTERN = re.compile(
    rb'new-object\s+System\.Net\.NetworkCredential\([^,]+,\s*["\'][^"\']+["\']',
    re.IGNORECASE,
)

# CSCAN0200 - DevDiv TFVC credentials
AZURE_DEVTFVC_PATTERN = re.compile(
    rb"enc_username=.+[\n\r\s]+enc_password=.{3,}",
)

# CSCAN0240 - DevOps Personal Access Token
AZURE_DEVOPS_PAT_PATTERN = re.compile(
    rb'access_token.*?[\'="][a-zA-Z0-9/+]{10,99}["\']',
    re.IGNORECASE,
)

# CSCAN0030 - PublishSettings userPWD
PUBLISHSETTINGS_PWD_PATTERN = re.compile(
    rb'userPWD="[a-zA-Z0-9/\\+]{60}"',
)

# CSCAN0060 - PEM certificate files with private key
PEM_PRIVATE_KEY_PATTERN = re.compile(
    rb"-{5}BEGIN( ([DR]SA|EC|OPENSSH))? PRIVATE KEY-{5}",
)

# CSCAN0080 - SecurityConfig XML passwords
SECURITY_CONFIG_PASSWORD_PATTERN = re.compile(
    rb"<[pP]ass[wW]ord>[^<]+</[pP]ass[wW]ord>",
)

# CSCAN0110 - Script passwords in PowerShell/CMD
SCRIPT_PASSWORD_PATTERN = re.compile(
    rb'\s-([pP]ass[wW]ord|PASSWORD)\s+(["\'][^"\'\r\n]*["\']|[^$\(\)\[\{<\-\r\n]+\s*(\r\n|\-))',
)

# CSCAN0111 - General password patterns
GENERAL_PASSWORD_PATTERN = re.compile(
    rb'[a-zA-Z_\s](([pP]ass[wW]ord)|PASSWORD|([cC]lient|CLIENT|[aA]pp|APP)_?([sS]ecret|SECRET))\s{0,3}=\s{0,3}[\'"][^\s"\']{2,200}?[\'"][;\s]',
)

# CSCAN0210 - Git credentials
GIT_CREDENTIALS_PATTERN = re.compile(
    rb"[hH][tT][tT][pP][sS]?://.+:.+@[^/]+\.[cC][oO][mM]",
)

# CSCAN0220 - Password contexts (ConvertTo-SecureString, X509Certificate2, etc.)
PASSWORD_CONTEXT_PATTERN = re.compile(
    rb'([cC]onvert[tT]o-[sS]ecure[sS]tring(\s*-[sS]tring)?\s*"[^"\r\n]+"|new\sX509Certificate2\([^()]*,\s*"[^"\r\n]+"|<[pP]ass[wW]ord>(<[vV]alue>)?.+(</[vV]alue>)?</[pP]ass[wW]ord>|([cC]lear[tT]ext[pP]ass[wW]ord|CLEARTEXTPASSWORD)("?)?\s*[:=]\s*"[^"\r\n]+")',
)

# CSCAN0230 - Slack tokens
SLACK_TOKEN_PATTERN = re.compile(
    rb"xoxp-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+|xoxb-[a-zA-Z0-9]+-[a-zA-Z0-9]+",
)

# CSCAN0250 - OAuth/JWT tokens and refresh tokens
JWT_TOKEN_PATTERN = re.compile(
    rb"eyJ[a-zA-Z0-9\-_%]+\.eyJ[a-zA-Z0-9\-_%]+\.[a-zA-Z0-9\-_%]+",
)

REFRESH_TOKEN_PATTERN = re.compile(
    rb'([rR]efresh_?[tT]oken|REFRESH_?TOKEN)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_]+-)+[a-zA-Z0-9_]+["\']?',
)

# CSCAN0260 - Ansible Vault (corrected from CSCAN0270)
ANSIBLE_VAULT_PATTERN = re.compile(
    rb"\$ANSIBLE_VAULT;[0-9]\.[0-9];AES256[\r\n]+\d+",
)

# CSCAN0270 - Azure PowerShell Token Cache
AZURE_POWERSHELL_TOKEN_PATTERN = re.compile(
    rb'["\']TokenCache["\']\s*:\s*\{\s*["\']CacheData["\']\s*:\s*["\'][a-zA-Z0-9/\+]{86}',
)

# CSCAN0140 - Default/known passwords
DEFAULT_PASSWORDS_PATTERN = re.compile(
    rb"(T!T@n1130|[pP]0rsche911|[cC]o[mM][mM]ac\!12|[pP][aA]ss@[wW]or[dD]1|[rR]dP[aA]\$\$[wW]0r[dD]|iis6\!dfu|[pP]@ss[wW]or[dD]1|[pP][aA]\$\$[wW]or[dD]1|\!\!123ab|[aA]dmin123|[pP]@ss[wW]0r[dD]1|[uU]ser@123|[aA]bc@123|[pP][aA]ss[wW]or[dD]@123|homerrocks|[pP][aA]\$\$[wW]0r[dD]1?|Y29NbWFjITEy|[pP][aA]ss4Sales|WS2012R2R0cks\!|DSFS0319Test|March2010M2\!|[pP][aA]ss[wW]ord~1|[mM]icr0s0ft|test1test\!|123@tieorg|homerocks|[eE]lvis1)",
)


PATTERNS = [
    ("datafactory-shir", AZURE_DATAFACTORY_SHIR_PATTERN),
    ("app-service-deployment", AZURE_APP_SERVICE_DEPLOYMENT_PATTERN),
    ("publishsettings-pwd", PUBLISHSETTINGS_PWD_PATTERN),
    ("storage-86char", AZURE_STORAGE_86CHAR_PATTERN),
    ("storage-43char", AZURE_STORAGE_43CHAR_PATTERN),
    ("storage-sig", AZURE_STORAGE_SIG_PATTERN),
    ("storage-useridpw", AZURE_STORAGE_USERIDPW_PATTERN),
    ("storage-accountkey", AZURE_STORAGE_ACCOUNTKEY_PATTERN),
    ("storage-servicebus", AZURE_STORAGE_SERVICEBUS_PATTERN),
    ("storage-moniker", AZURE_STORAGE_MONIKER_PATTERN),
    ("storage-bloburl", AZURE_STORAGE_BLOBURL_PATTERN),
    ("password-machinekey", AZURE_PASSWORD_MACHINEKEY_PATTERN),
    ("password-addkey", AZURE_PASSWORD_ADDKEY_PATTERN),
    ("password-connstring", AZURE_PASSWORD_CONNSTRING_PATTERN),
    ("password-value", AZURE_PASSWORD_VALUE_PATTERN),
    ("password-uidpw", AZURE_PASSWORD_UIDPW_PATTERN),
    ("network-credential", AZURE_NETWORK_CREDENTIAL_PATTERN),
    ("network-schtasks", AZURE_NETWORK_SCHTASKS_PATTERN),
    ("network-dotnet", AZURE_NETWORK_DOTNET_PATTERN),
    ("devtfvc-secrets", AZURE_DEVTFVC_PATTERN),
    ("devops-pat", AZURE_DEVOPS_PAT_PATTERN),
    ("pem-private-key", PEM_PRIVATE_KEY_PATTERN),
    ("security-config-password", SECURITY_CONFIG_PASSWORD_PATTERN),
    ("script-password", SCRIPT_PASSWORD_PATTERN),
    ("general-password", GENERAL_PASSWORD_PATTERN),
    ("git-credentials", GIT_CREDENTIALS_PATTERN),
    ("password-context", PASSWORD_CONTEXT_PATTERN),
    ("slack-token", SLACK_TOKEN_PATTERN),
    ("jwt-token", JWT_TOKEN_PATTERN),
    ("refresh-token", REFRESH_TOKEN_PATTERN),
    ("ansible-vault", ANSIBLE_VAULT_PATTERN),
    ("azure-powershell-token", AZURE_POWERSHELL_TOKEN_PATTERN),
    ("default-passwords", DEFAULT_PASSWORDS_PATTERN),
]


def check_file_for_azure_keys(
    filenames: Sequence[str],
) -> list[BadFile]:
    """Check if files contain Azure credentials.

    Return a list of all files containing Azure credentials with the keys
    obfuscated to ease debugging.
    """
    bad_files = []

    for filename in filenames:
        with open(filename, "rb") as content:
            text_body = content.read()

            # Check all Azure credential patterns
            for pattern_name, pattern in PATTERNS:
                matches = pattern.findall(text_body)
                for match in matches:
                    # Handle tuple results from regex groups
                    if isinstance(match, tuple):
                        match = match[0]

                    # Obfuscate the key
                    key_str = match.decode("utf-8", errors="replace")
                    if len(key_str) > 20:
                        key_hidden = key_str[:10] + "***" + key_str[-7:]
                    else:
                        key_hidden = key_str[:4] + "***"

                    bad_files.append(
                        BadFile(filename, key_hidden, pattern_name),
                    )

    return bad_files


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+", help="Filenames to run")
    args = parser.parse_args(argv)

    bad_filenames = check_file_for_azure_keys(args.filenames)
    if bad_filenames:
        for bad_file in bad_filenames:
            print(
                f"Azure credential ({bad_file.pattern_name}) found in "
                f"{bad_file.filename}: {bad_file.key}",
            )
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
