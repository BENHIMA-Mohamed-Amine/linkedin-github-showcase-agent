

def register_mc_prompt(mcp):
    """
    Register a multiple-choice prompt with the given name and prompt text.
    
    Args:
        name (str): The name of the prompt.
        prompt (str): The text of the prompt.
    """
    
    @mcp.prompt
    def prompt_to_generate_linkedin_post() -> str:
        """
        prompt to generate a LinkedIn post about the project.
        
        Returns:
            str: The prompt for generating LinkedIn post.
        """
        
        return """
        You are an expert LinkedIn post writer.
        Write a LinkedIn post about this project.
        use the tools that you have to get the project information that you need.
        your post should follow this format:
        1. Start with a catchy title.
        2. Tell the story of the project and motivation behind it.
        3. Highlight the problems it solves.
        4. Mention the tech stack used.
        5. Include relevant hashtags to increase the visibility.
        Your tone should be professional, clear and concise.
        """