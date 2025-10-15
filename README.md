# Samsung User-Agent Generator

A Python tool that generates realistic Samsung smartphone user-agent strings for both global and USA markets. Useful for web scraping, testing, and development scenarios requiring authentic mobile browser signatures.

## Features

- 🎯 Generates unique, realistic Samsung device user-agents
- 🌍 Supports both global and USA market models with weighted distributions
- 🔧 Customizable Android versions and Chrome versions
- 🔒 Prevents duplicates when generating in multiple runs
- ⚖️ Configurable USA vs. Global ratio
- 💻 Command-line interface for easy usage
- 📊 JSON output format for easy integration

## Requirements

- Python 3.6 or higher
- Standard Python libraries (no external dependencies)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rakibroni2468/samsung-ua-generator.git
   cd samsung-ua-generator
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

### Basic Usage

Run with default settings (generates 20 user-agents with 50% USA devices):

```bash
python samsung_ua_generator.py
```

### Custom Parameters

```bash
# Generate 50 user-agents with 70% USA devices
python samsung_ua_generator.py -n 50 --usa-ratio 0.7

# Generate 100 user-agents and save to custom file
python samsung_ua_generator.py -n 100 -o my_user_agents.json

# Enable debug logging for detailed process information
python samsung_ua_generator.py --log-level DEBUG

# Combine multiple options
python samsung_ua_generator.py -n 200 --usa-ratio 0.3 -o global_heavy.json --log-level INFO
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-n`, `--number` | Number of user-agents to generate | `20` |
| `-o`, `--output` | Output filename | `unique_samsung_us_global_ua.json` |
| `--usa-ratio` | Proportion of USA devices (0.0-1.0) | `0.5` |
| `--log-level` | Logging verbosity (DEBUG/INFO/WARNING/ERROR) | `INFO` |

## Output Format

The tool generates a JSON file containing an array of user-agent strings:

```json
[
  "Mozilla/5.0 (Linux; Android 14; SM-S918U Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
  "Mozilla/5.0 (Linux; Android 13; SM-A536B Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
  ...
]
```

## How It Works

The generator uses weighted probability distributions to create realistic user-agent strings:

### 1. **Device Selection**
- Different Samsung models for USA (SM-XXXU suffix) and Global (SM-XXXB/F/N suffix) markets
- Weighted distribution favoring popular models (Galaxy S and A series)
- Authentic model numbers matching real Samsung devices

### 2. **Android Version**
- Versions 11 through 14 with higher weights for recent releases
- Realistic version distribution matching market statistics

### 3. **Chrome Version**
- Versions 115-122 based on actual Chrome browser usage
- Weighted toward newer versions while maintaining realistic diversity

### 4. **Build Tags**
- Authentic-looking Android build identifiers (e.g., TP1A.220624.014)
- Follows Google's build tag format conventions

### 5. **Duplicate Prevention**
- Loads existing user-agents from output file on startup
- Validates uniqueness before adding new entries
- Appends only new user-agents to maintain historical data

## Use Cases

- **Web Scraping**: Rotate through realistic mobile user-agents to avoid detection
- **Testing**: Simulate Samsung device traffic for mobile web testing
- **Analytics**: Generate test data for user-agent parsing systems
- **Development**: Mock mobile device requests during development
- **Load Testing**: Create diverse traffic patterns for stress testing

## Example Workflow

```bash
# Generate initial set with USA focus
python samsung_ua_generator.py -n 50 --usa-ratio 0.8 -o usa_agents.json

# Generate global-focused set
python samsung_ua_generator.py -n 50 --usa-ratio 0.2 -o global_agents.json

# Generate balanced set with detailed logging
python samsung_ua_generator.py -n 100 --usa-ratio 0.5 --log-level DEBUG
```

## Tips and Best Practices

- **Start Small**: Test with `-n 10` before generating large batches
- **Monitor Output**: Use `--log-level DEBUG` to understand the generation process
- **Avoid Over-generation**: Generate only what you need to keep the dataset manageable
- **Regular Updates**: Regenerate periodically to include newer Chrome versions
- **Backup Data**: Keep copies of your generated user-agent files
- **Respect Websites**: Use generated user-agents responsibly and follow robots.txt

## Troubleshooting

**Issue**: Script shows "duplicate" warnings
- **Solution**: This is normal behavior preventing duplicates. The script will keep trying until it generates unique entries.

**Issue**: Permission denied when writing output file
- **Solution**: Check file permissions or specify a different output path with `-o`

**Issue**: Want to reset and start fresh
- **Solution**: Delete or rename the existing JSON output file

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests for:
- Additional Samsung device models
- Updated Chrome version distributions
- New features or improvements
- Bug fixes and documentation enhancements

## License

This project is provided as-is for educational and development purposes. Please use responsibly and in accordance with applicable laws and website terms of service.

## Disclaimer

This tool generates synthetic user-agent strings for testing and development purposes. Users are responsible for ensuring their use complies with applicable laws, terms of service, and ethical guidelines. The authors assume no liability for misuse of this tool.

## Contact

For questions, suggestions, or issues, please open an issue on the GitHub repository.

---

**Made with ❤️ for developers who need realistic Samsung user-agents**
