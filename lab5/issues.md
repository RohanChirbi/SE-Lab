# Lab 5: Static Code Analysis Issues

## Program

File: smart_home.py

Line numbers refer to the original source code, not the cleaned version.

Issues are ordered by potential impact. Severity labels below are
project-level assessments, not necessarily tool-assigned severities.
Manual findings are distinguished from static-analysis checks.

## Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Unsafe shell execution | High — Security; Bandit B602 | 49–51 | runScene concatenated a supplied script name into a command executed with shell=True. Untrusted input reaching this function could execute unintended commands. | Removed the unused scene-execution helper and subprocess import. The required controller demonstration does not use this helper. |
| Shared mutable default settings | Medium — Bug; Pylint W0102 | 11–13 | The default settings={} dictionary was shared by devices created without explicit settings. Updating the thermostat also added temperature settings to unrelated devices, including the light. | Replaced the default with None, created independent settings for each device, and deep-copied caller-supplied dictionaries. |
| Hard-coded password | Medium — Security; Bandit B105 | 7 | An unused password literal was stored in source code. Although not used for authentication, it could become a security risk if activated later. | Removed the unused password constant. |
| All-interface hub address | Medium — Security configuration; Bandit B104 | 4 | The address 0.0.0.0 would bind all IPv4 interfaces if used by a server. This script only prints the address and does not actually start a listener. | Changed the default hub address to 127.0.0.1 for local-only configuration. |
| Unknown thermostat device causes an exception | Medium — Robustness; manual inspection | 23–24 | Direct access to devices[deviceName] raised KeyError when the requested device did not exist. | Added an existence check, a clear message, and a False return before accessing the device. |
| Missing temperature input validation | Medium — Robustness; manual inspection | 23–28 | Temperature handling assumed numeric input. Strings or None could raise errors, while Boolean and non-finite values were not explicitly rejected. | Added numeric validation, rejected Boolean and non-finite values, and preserved the original 16–30 degree clamping behaviour. |
| Unsupported device types accepted | Low — Validation; manual inspection | 11–13, 38 | Arbitrary device kinds were accepted, and unknown kinds silently contributed zero watts to the power calculation. | Validate device kinds against POWER_USAGE and raise ValueError for unsupported kinds. |
| Missing settings type validation | Low — Robustness; manual inspection | 11–13, 28 | Non-dictionary settings could cause failures when the program attempted to update a setting. | Accept only a dictionary or None and raise TypeError for other values. |
| Inconsistent return paths | Low — Maintainability; Pylint R1710 | 16–20 | toggleDevice returned a Boolean for an existing device but implicitly returned None for an unknown device. | Added an explicit None return and documented the Boolean-or-None behaviour. |
| Missing explicit file encoding | Low — Portability; Pylint W1514 | 40–42 | The JSON output file used the platform-dependent default encoding. | Open the output file with encoding="utf-8". |
| Non-standard function and parameter names | Low — Style; Pylint C0103 | 11, 16, 23, 32, 36, 40, 45, 49 | Names such as addDevice, deviceName, and fileName did not follow Python snake_case conventions. | Renamed retained functions and parameters to snake_case and updated their references. Named the module-level registry DEVICES. |
| Missing documentation | Low — Maintainability; Pylint C0114/C0116 | 1, 11, 16, 23, 32, 36, 40, 45, 49, 54 | The module and public functions lacked docstrings explaining their purpose and behaviour. | Added a module docstring and concise docstrings to all retained functions. |
| Whitespace and blank-line violations | Low — Style; Flake8 E203/E302/E261 | 6, 40, 66 | The original code had whitespace before a dictionary colon, insufficient separation before a top-level function, and insufficient spacing before an inline comment. | Corrected dictionary formatting and function separation, and removed the affected inline comment during cleanup. |
| Program executes during import | Low — Maintainability; manual inspection | 72 | The unconditional main() call executed the demonstration and wrote a JSON file when the module was imported. | Added an if __name__ == "__main__": guard. |

## Verified Analysis Results

| Tool | Before fixes | After fixes |
|------|--------------|-------------|
| Pylint | 4.60/10 | 10.00/10; no diagnostic messages |
| Bandit | Security findings recorded in the baseline report | No issues identified; zero low-, medium-, or high-severity findings |
| Flake8 | Style findings recorded in the baseline report | No findings; final report is empty |

The Pylint score increased by 5.40 points and exceeds the target of
9.5/10. The final Bandit and Flake8 reports contain no findings.

These results verify static-analysis cleanliness. They do not replace
runtime testing or prove the absence of every possible defect.

## Report Locations

### Before Fixes

- reports/before/pylint_report.txt
- reports/before/bandit_report.txt
- reports/before/flake8_report.txt
- reports/before/demo_output.txt

### After Fixes

- reports/after/pylint_report.txt
- reports/after/bandit_report.txt
- reports/after/flake8_report.txt

## Functional Changes

The cleaned implementation retains:

- Adding devices to rooms.
- Switching devices on and off.
- Setting thermostat temperatures within the existing safe range.
- Listing devices by room.
- Calculating active-device power use.
- Saving the current state to home_state.json.

The unused shell-execution helper was removed deliberately because
the required controller demonstration does not use it.

Device settings now have independent storage. Setting the thermostat
temperature no longer modifies the light's settings. The original
clamping behaviour is preserved: requesting 35 degrees stores 30.

Unknown devices and invalid temperature inputs are handled explicitly.
The module can also be imported without automatically running the
demonstration or writing the state file.
