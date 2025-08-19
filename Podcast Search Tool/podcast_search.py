#!/usr/bin/env python3
"""
Intelligent Podcast Search Tool using Agno Framework
Searches Listen Notes and Podscan APIs with natural language processing
"""

import os
import requests
import json
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Try different possible agno import patterns
try:
    from agno import Agent, tool
    AGNO_AVAILABLE = True
except ImportError:
    try:
        from agno import Agno as Agent, tool
        AGNO_AVAILABLE = True
    except ImportError:
        try:
            from agno.agent import Agent
            from agno.tools import tool
            AGNO_AVAILABLE = True
        except ImportError:
            print("⚠️  Agno not available, running in standard mode.")
            AGNO_AVAILABLE = False
            # Fallback: Create dummy decorators
            def Agent(*args, **kwargs):
                def decorator(cls):
                    return cls
                return decorator
            
            def tool(func):
                return func

# Load environment variables from .env file
load_dotenv()

# API Configuration
LISTEN_NOTES_API_KEY = os.getenv("LISTEN_NOTES_API_KEY", "")
PODSCAN_API_KEY = os.getenv("PODSCAN_API_KEY", "")

LISTEN_NOTES_BASE_URL = "https://listen-api.listennotes.com/api/v2"
PODSCAN_BASE_URL = "https://podscan.fm/api/v1"

@tool
def search_listen_notes_tool(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search podcasts using Listen Notes API - Tool version for Agno framework"""
    return search_listen_notes_direct(query, limit)

@tool  
def search_podscan_tool(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search podcasts using Podscan API - Tool version for Agno framework"""
    return search_podscan_direct(query, limit)

def search_listen_notes_direct(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search podcasts using Listen Notes API - Direct function call"""
    """Search podcasts using Listen Notes API"""
    if not LISTEN_NOTES_API_KEY:
        return []
    
    headers = {
        'X-ListenAPI-Key': LISTEN_NOTES_API_KEY
    }
    
    params = {
        'q': query,
        'type': 'podcast',
        'page_size': min(limit, 50),  # Listen Notes max is 50
        'language': 'English'
    }
    
    try:
        response = requests.get(
            f"{LISTEN_NOTES_BASE_URL}/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for podcast in data.get('results', []):
                result = {
                    'title': podcast.get('title_original', ''),
                    'host': podcast.get('publisher_original', 'Unknown Host'),
                    'description': podcast.get('description_original', ''),
                    'link': podcast.get('website', podcast.get('listennotes_url', '')),
                    'source': 'Listen Notes'
                }
                results.append(result)
            
            return results
        else:
            print(f"Listen Notes API returned status code: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"Error searching Listen Notes: {e}")
        return []

def search_podscan_direct(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search podcasts using Podscan API - Direct function call"""
    """Search podcasts using Podscan API"""
    if not PODSCAN_API_KEY:
        return []
    
    headers = {
        'Authorization': f'Bearer {PODSCAN_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'query': query,
        'per_page': min(limit, 50),  # Podscan max is 50
        'order_by': 'best_match',
        'search_fields': 'name,description,publisher_name',
        'language': 'en'
    }
    
    try:
        response = requests.get(
            f"{PODSCAN_BASE_URL}/podcasts/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for podcast in data.get('podcasts', []):
                result = {
                    'title': podcast.get('podcast_name', ''),
                    'host': podcast.get('publisher_name', 'Unknown Host'),
                    'description': podcast.get('podcast_description', ''),
                    'link': podcast.get('podcast_url', ''),
                    'source': 'Podscan'
                }
                results.append(result)
            
            return results
        else:
            print(f"Podscan API returned status code: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"Error searching Podscan: {e}")
        return []

class PodcastSearchAgent:
    """Intelligent podcast search agent that understands natural language queries"""
    
    def __init__(self):
        self.topic_keywords = {
            'technology': ['tech', 'programming', 'coding', 'software', 'ai', 'machine learning', 'javascript', 'python', 'react', 'frontend', 'backend'],
            'business': ['startup', 'entrepreneur', 'marketing', 'sales', 'finance', 'investment', 'leadership'],
            'health': ['fitness', 'nutrition', 'wellness', 'mental health', 'meditation', 'mindfulness'],
            'entertainment': ['comedy', 'movies', 'tv shows', 'celebrity', 'pop culture'],
            'education': ['learning', 'science', 'history', 'philosophy', 'research'],
            'news': ['politics', 'current events', 'journalism', 'world news'],
            'sports': ['football', 'basketball', 'soccer', 'baseball', 'fitness', 'athletics'],
            'crime': ['true crime', 'mystery', 'investigation', 'detective', 'murder'],
            'lifestyle': ['travel', 'food', 'fashion', 'relationships', 'parenting']
        }
    
    def parse_natural_language(self, user_input: str) -> Dict[str, Any]:
        """Parse natural language input to extract search intent and parameters"""
        user_input = user_input.lower().strip()
        
        # Extract sorting preferences
        sort_method = "mixed"  # default
        if any(phrase in user_input for phrase in ['alphabetical', 'a to z', 'alphabetically']):
            sort_method = "title"
        elif any(phrase in user_input for phrase in ['by host', 'by publisher', 'by creator']):
            sort_method = "host"
        elif any(phrase in user_input for phrase in ['by source', 'grouped by', 'separate']):
            sort_method = "source"
        elif any(phrase in user_input for phrase in ['no sorting', 'unsorted', 'random']):
            sort_method = "none"
        
        results_per_source = 20 
        
        # Extract and enhance search terms
        search_terms = self.enhance_search_terms(user_input)
        
        return {
            'search_terms': search_terms,
            'sort_method': sort_method,
            'results_per_source': results_per_source,
            'original_query': user_input
        }
    
    def enhance_search_terms(self, user_input: str) -> str:
        """Enhance search terms by expanding topics and removing stop words"""
        # Remove common stop phrases for podcast search
        stop_phrases = [
            'find me', 'search for', 'looking for', 'show me', 'i want',
            'podcasts about', 'podcasts on', 'podcasts for', 'podcasts',
            'podcast', 'episodes', 'shows', 'audio', 'listen to'
        ]
        
        enhanced_query = user_input
        for phrase in stop_phrases:
            enhanced_query = enhanced_query.replace(phrase, '')
        
        # Clean up extra spaces
        enhanced_query = ' '.join(enhanced_query.split())
        
        # If the query matches topic categories, enhance with related keywords
        for topic, keywords in self.topic_keywords.items():
            if any(keyword in enhanced_query for keyword in keywords):
                # Add the topic name to improve search
                if topic not in enhanced_query:
                    enhanced_query = f"{topic} {enhanced_query}"
                break
        
        return enhanced_query.strip()
    
    def remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on title similarity"""
        unique_results = []
        seen_titles = set()
        
        for result in results:
            title_key = result['title'].lower().strip()
            if title_key not in seen_titles and title_key:
                seen_titles.add(title_key)
                unique_results.append(result)
        
        return unique_results
    
    def sort_results(self, results: List[Dict[str, Any]], sort_method: str = "mixed") -> List[Dict[str, Any]]:
        """Sort results using different methods"""
        if not results:
            return results
            
        if sort_method == "mixed":
            # Alternate between sources for balanced display, but allow uneven distribution
            listen_notes = [r for r in results if r['source'] == 'Listen Notes']
            podscan = [r for r in results if r['source'] == 'Podscan']
            
            mixed_results = []
            ln_idx = 0
            ps_idx = 0
            
            # Alternate between sources until we've used all results
            while ln_idx < len(listen_notes) or ps_idx < len(podscan):
                if ln_idx < len(listen_notes):
                    mixed_results.append(listen_notes[ln_idx])
                    ln_idx += 1
                if ps_idx < len(podscan):
                    mixed_results.append(podscan[ps_idx])
                    ps_idx += 1
            
            return mixed_results
            
        elif sort_method == "source":
            return sorted(results, key=lambda x: (x['source'], x['title']))
            
        elif sort_method == "title":
            return sorted(results, key=lambda x: x['title'].lower())
            
        elif sort_method == "host":
            return sorted(results, key=lambda x: x['host'].lower())
            
        elif sort_method == "none":
            return results
            
        else:
            return self.sort_results(results, "mixed")
    
    def format_description(self, description: str, max_sentences: int = 3) -> str:
        """Format description to 2-3 sentences"""
        if not description:
            return "No description available."
        
        # Clean up HTML tags if present
        description = re.sub('<[^<]+?>', '', description)
        
        # Split into sentences
        sentences = description.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Return first 2-3 sentences
        return '. '.join(sentences[:max_sentences]) + '.' if sentences else "No description available."
    
    def display_results(self, results: List[Dict[str, Any]], query_info: Dict[str, Any]):
        """Display search results in a formatted way"""
        if not results:
            print("No podcasts found.")
            return
        
        print(f"\n🎧 Found {len(results)} podcast(s) for: '{query_info['original_query']}'")
        print(f"🔍 Search terms: '{query_info['search_terms']}'")
        print(f"📊 Sorting: {query_info['sort_method']}\n")
        
        for i, result in enumerate(results, 1):
            print(f"{'='*60}")
            print(f"#{i} - {result['title']}")
            print(f"{'='*60}")
            print(f"📻 Host: {result['host']}")
            print(f"📝 Description: {self.format_description(result['description'])}")
            print(f"🔗 Link: {result['link']}")
            print(f"📊 Source: {result['source']}")
            print()
    
    def search_podcasts(self, natural_language_query: str) -> str:
        """
        Main method: Search for podcasts using natural language input
        """
        # Parse the natural language query
        query_info = self.parse_natural_language(natural_language_query)
        
        print(f"🧠 Enhanced search: '{query_info['search_terms']}'")
        print(f"📊 Sorting: {query_info['sort_method']}")
        print(f"🎯 Showing top 10 results\n")
        
        # Search both APIs with higher limits to ensure 10 unique results
        listen_notes_results = search_listen_notes_direct(query_info['search_terms'], 20)  # Request 20 from each
        podscan_results = search_podscan_direct(query_info['search_terms'], 20)
        
        # Ensure both results are lists
        if listen_notes_results is None:
            listen_notes_results = []
        if podscan_results is None:
            podscan_results = []
        
        # Combine results
        all_results = listen_notes_results + podscan_results
        
        # Remove duplicates
        unique_results = self.remove_duplicates(all_results)
        
        # Sort results using specified method
        sorted_results = self.sort_results(unique_results, query_info['sort_method'])
        
        # Limit to 10 results for display
        final_results = sorted_results[:10]
        
        # Display results
        self.display_results(final_results, query_info)
        
        ln_count = len([r for r in final_results if r['source'] == 'Listen Notes'])
        ps_count = len([r for r in final_results if r['source'] == 'Podscan'])
        
        return f"Search completed. Showing top {len(final_results)} unique podcast(s) ({ln_count} from Listen Notes, {ps_count} from Podscan)."

def main():
    """Main function to run the intelligent podcast search tool"""
    print("🎧 Intelligent Podcast Search Tool")
    if AGNO_AVAILABLE:
        print("Powered by Agno Framework")
    print("=" * 50)
    
    # Initialize the agent
    if AGNO_AVAILABLE:
        try:
            # Try to create an Agno agent
            agno_agent = Agent()
            # Add our search method to the agent
            agno_agent.search_podcasts = PodcastSearchAgent().search_podcasts
            agent = agno_agent
        except Exception as e:
            print(f"⚠️  Could not initialize Agno agent: {e}")
            print("Running in standard mode...")
            agent = PodcastSearchAgent()
    else:
        agent = PodcastSearchAgent()
    
    # Check for API keys
    if not LISTEN_NOTES_API_KEY and not PODSCAN_API_KEY:
        print("⚠️  Warning: No API keys found.")
        print("Create a .env file with LISTEN_NOTES_API_KEY and/or PODSCAN_API_KEY.")
        print("You can still run the tool, but searches may not work.\n")
    elif LISTEN_NOTES_API_KEY and not PODSCAN_API_KEY:
        print("ℹ️  Using Listen Notes API only.")
    elif not LISTEN_NOTES_API_KEY and PODSCAN_API_KEY:
        print("ℹ️  Using Podscan API only.")
    else:
        print("✅ Using both Listen Notes and Podscan APIs.")
    
    print("\n🧠 Natural Language Examples:")
    print("  • 'Find me JavaScript programming podcasts'")
    print("  • 'Show me true crime shows sorted alphabetically'")
    print("  • 'I want business podcasts about startups'")
    print("  • 'Comedy podcasts grouped by source'")
    print("  • 'Meditation and mindfulness shows'")
    print("  • Always shows top 10 most relevant results")
    
    while True:
        try:
            # Get user input
            query = input("\n🎙️ Describe what podcasts you're looking for (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            # Run the intelligent search
            if hasattr(agent, 'search_podcasts'):
                result = agent.search_podcasts(query)
            else:
                # Fallback for standard agent
                search_agent = PodcastSearchAgent()
                result = search_agent.search_podcasts(query)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()