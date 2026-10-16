# Lab 5: Static Code Analysis Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues were formatting violations, non-standard names,
missing docstrings, and missing file encoding. The tools identified
specific locations, and the corrections required little change to
the program's logic.

The shared mutable default argument was harder to understand because
the program still ran, but updating the thermostat also changed the
light's settings. The cause was that multiple devices shared the
same default dictionary. Replacing the default with None and creating
independent settings for each device corrected the underlying problem.
Deep-copying supplied settings also prevents nested values from being
shared accidentally.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

The Bandit warning about the address 0.0.0.0 required contextual review.
That address can expose a server on all network interfaces, but this
program only displayed the configured address; it did not actually
start a server.

Therefore, the warning did not indicate an actively exposed service
in this implementation. I treated it as a precautionary configuration
warning rather than proof of an exploitable vulnerability. I changed
the default to 127.0.0.1 to make the intended local configuration clear.

This showed that static-analysis findings must be interpreted in the
context of how the flagged code is actually used.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would install Pylint, Bandit, and Flake8 in the project's virtual
environment and run them regularly during development and before
committing changes.

I would automate these checks using pre-commit hooks and a continuous
integration pipeline. Security and correctness findings would receive
priority, followed by maintainability and style improvements.

I would also use unit tests and runtime checks because static analysis
cannot confirm every behavioural requirement. Any suppressed warning
would need a documented justification rather than being ignored simply
to improve the score.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The Pylint score increased from 4.60/10 to 10.00/10. The final Bandit
report identified no issues, and the final Flake8 report contained no
findings.

The code became easier to read through snake_case naming, consistent
formatting, and module and function docstrings. Removing the unused
shell-execution helper and hard-coded password reduced unnecessary
security risks.

Device settings now have independent storage, preventing thermostat
updates from affecting unrelated devices. Explicit checks handle
unknown devices and invalid temperature inputs while preserving the
original 16–30 degree clamping behaviour.

Explicit UTF-8 encoding makes JSON persistence more predictable across
systems. The main guard also allows the module to be imported without
automatically running the demonstration or writing the state file.

These improvements increase maintainability and potential robustness,
but clean static-analysis reports do not prove that every possible
runtime defect has been eliminated.
