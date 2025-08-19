# 🎧 Intelligent Podcast Search Tool

An AI-powered command-line tool that searches multiple podcast APIs using natural language queries. Built with the Agno framework for intelligent query processing and enhanced search capabilities.

## ✨ Features

- 🧠 **Natural Language Processing** - Describe what you want in plain English
- 🔍 **Dual API Search** - Searches both Listen Notes and Podscan APIs
- 📊 **Smart Query Enhancement** - Automatically expands search terms for better results
- 🎯 **Guaranteed 10 Results** - Always returns 10 high-quality, unique podcasts
- 📱 **Multiple Sorting Options** - Mixed, alphabetical, by host, or by source
- 🚫 **Intelligent Deduplication** - Removes duplicate podcasts across APIs
- 💬 **Interactive Terminal UI** - Clean, user-friendly command-line interface

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AleksPGL/podcast-search-tool.git
   cd podcast-search-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys**
   
   Create a `.env` file in the project directory:
   ```env
   LISTEN_NOTES_API_KEY=your_listen_notes_api_key_here
   PODSCAN_API_KEY=your_podscan_api_key_here
   ```

4. **Run the tool**
   ```bash
   python podcast_search.py
   ```

## 🔑 API Keys Setup

### Listen Notes API
1. Sign up at [Listen Notes API](https://www.listennotes.com/api/)
2. Get your free API key (100 requests/month)
3. Add to your `.env` file

### Podscan API  
1. Sign up at [Podscan](https://podscan.fm/)
2. Get your API key from the dashboard
3. Add to your `.env` file

> **Note:** The tool works with either API key, but having both provides the best results.

## 💬 Natural Language Examples

Instead of structured queries, just describe what you're looking for:

```bash
🎙️ Describe what podcasts you're looking for: Find me JavaScript programming podcasts

🎙️ Describe what podcasts you're looking for: Show me true crime shows sorted alphabetically

🎙️ Describe what podcasts you're looking for: I want business podcasts about startups

🎙️ Describe what podcasts you're looking for: Comedy podcasts grouped by source

🎙️ Describe what podcasts you're looking for: Meditation and mindfulness shows
```

## 🧠 Smart Query Processing

The tool automatically enhances your search:

| Your Input | Enhanced Search | Why |
|------------|----------------|-----|
| "javascript podcasts" | "technology javascript programming" | Adds related tech terms |
| "true crime stories" | "crime true crime mystery" | Expands crime category |
| "business startups" | "business startup entrepreneur" | Includes entrepreneurship |
| "meditation shows" | "health meditation mindfulness" | Adds wellness context |

## 📊 Sorting Options

Control how results are displayed by adding sorting terms to your query:

- **Mixed (default)** - Alternates between API sources for variety
- **Alphabetically** - Say "alphabetically" or "a to z"
- **By Host** - Say "by host" or "by publisher"  
- **By Source** - Say "by source" or "grouped by"
- **No Sorting** - Say "unsorted" or "random"

### Examples:
```bash
"javascript podcasts sorted alphabetically"
"true crime shows by host"
"business podcasts grouped by source"
```

## 🎯 Sample Output

```
🎧 Found 10 podcast(s) for: 'javascript programming'
🔍 Search terms: 'technology javascript programming'
📊 Sorting: mixed

============================================================
#1 - JavaScript Jabber
============================================================
📻 Host: TopEndDevs
📝 Description: A weekly discussion about JavaScript, front-end development, community, careers, and frameworks.
🔗 Link: https://javascriptjabber.com/
📊 Source: Listen Notes

============================================================
#2 - Syntax - Tasty Web Development Treats
============================================================
📻 Host: Wes Bos & Scott Tolinski
📝 Description: Full Stack Developers Wes Bos and Scott Tolinski dive deep into web development.
🔗 Link: https://syntax.fm/
📊 Source: Podscan

... (8 more results)

Search completed. Showing top 10 unique podcast(s) (6 from Listen Notes, 4 from Podscan).
```

## 🏗️ Technical Architecture

### Built With
- **Python 3.7+**
- **Agno Framework** - For intelligent agent processing
- **Listen Notes API** - Comprehensive podcast database  
- **Podscan API** - Advanced podcast search and analytics
- **python-dotenv** - Environment variable management
- **requests** - HTTP API calls

### How It Works
1. **Natural Language Parsing** - Extracts intent, topics, and preferences
2. **Query Enhancement** - Expands search terms using topic categorization  
3. **Dual API Search** - Requests 20 results from each API (40 total)
4. **Smart Deduplication** - Removes duplicate podcasts across sources
5. **Intelligent Sorting** - Applies user-preferred sorting method
6. **Result Selection** - Returns top 10 unique, relevant podcasts

## 📋 Requirements

```
requests>=2.28.0
python-dotenv>=1.0.0
agno>=0.1.0
```

## 🎨 Topic Categories

The tool recognizes and enhances these topic categories:

| Category | Keywords |
|----------|----------|
| **Technology** | tech, programming, coding, AI, javascript, python |
| **Business** | startup, entrepreneur, marketing, sales, finance |
| **Health** | fitness, nutrition, wellness, mental health, meditation |
| **Entertainment** | comedy, movies, tv shows, celebrity, pop culture |
| **Education** | learning, science, history, philosophy, research |
| **Crime** | true crime, mystery, investigation, detective |
| **Sports** | football, basketball, soccer, fitness, athletics |
| **Lifestyle** | travel, food, fashion, relationships, parenting |

## 🔧 Configuration

### Environment Variables
- `LISTEN_NOTES_API_KEY` - Your Listen Notes API key
- `PODSCAN_API_KEY` - Your Podscan API key

### Customization
- Edit `topic_keywords` dictionary to add new categories
- Modify `results_per_source` to change API request limits
- Adjust `max_sentences` in `format_description()` for longer/shorter descriptions

## 🚦 Usage Tips

### Getting Better Results
- **Be specific**: "JavaScript React podcasts" vs "programming shows"
- **Use keywords**: Include technology names, topics, or genres
- **Try variations**: If no results, try broader or different terms
- **Sort strategically**: Use "mixed" for variety, "alphabetically" for browsing

### Troubleshooting
- **No results**: Try broader search terms or check API keys
- **Few results**: Some topics have limited podcast coverage
- **API errors**: Check internet connection and API key validity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contribution
- Add more podcast APIs (Spotify, Apple Podcasts, etc.)
- Improve natural language processing
- Add podcast recommendation features
- Create a web interface version
- Add podcast playlist/favorites functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Listen Notes](https://www.listennotes.com/)** - Comprehensive podcast database and API
- **[Podscan](https://podscan.fm/)** - Advanced podcast search and analytics
- **[Agno Framework](https://github.com/agno-ai/agno)** - Intelligent agent framework
- All the amazing podcast creators who make this content possible!

## 📞 Support

- Create an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Join discussions in the repository

---

**Made with ❤️ for podcast lovers everywhere**

*Find your next favorite podcast in seconds, not hours.*
