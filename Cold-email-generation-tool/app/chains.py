import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import json

load_dotenv()


class Chain:
    def __init__(self, user_config=None):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

        # Load user configuration or use defaults
        self.config = self.load_user_config() if user_config is None else user_config

    def load_user_config(self):
        """Load user configuration from file or environment variables"""
        config_file = "user_config.json"

        # Try to load from file first
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)

        # Otherwise, use environment variables or defaults
        return {
            "sender_name": os.getenv("SENDER_NAME", "Your Name"),
            "sender_title": os.getenv("SENDER_TITLE", "Business Development Executive"),
            "company_name": os.getenv("COMPANY_NAME", "Your Company"),
            "company_type": os.getenv("COMPANY_TYPE", "AI & Software Consulting"),
            "company_description": os.getenv("COMPANY_DESCRIPTION",
                                             "We are dedicated to facilitating the seamless integration of business processes through automated tools."),
            "company_achievements": os.getenv("COMPANY_ACHIEVEMENTS",
                                              "Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, process optimization, cost reduction, and heightened overall efficiency."),
            "email_tone": os.getenv("EMAIL_TONE", "professional"),  # professional, casual, formal
            "signature_style": os.getenv("SIGNATURE_STYLE", "standard")  # standard, detailed, minimal
        }

    def save_user_config(self, config):
        """Save user configuration to file"""
        with open("user_config.json", 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: 
            `role`, `experience`, `skills`, `description`, `company` (if mentioned), `location` (if mentioned).
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        # Determine email tone instructions
        tone_instructions = {
            "professional": "Write in a professional yet approachable tone.",
            "casual": "Write in a friendly, casual tone while maintaining professionalism.",
            "formal": "Write in a formal, corporate tone."
        }.get(self.config.get("email_tone", "professional"))

        # Determine signature style
        signature_instructions = {
            "standard": "End with a standard professional signature.",
            "detailed": "Include full contact details in the signature.",
            "minimal": "Use a minimal signature with just name and title."
        }.get(self.config.get("signature_style", "standard"))

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### YOUR IDENTITY AND COMPANY INFO:
            - Name: {sender_name}
            - Title: {sender_title}
            - Company: {company_name}
            - Company Type: {company_type}
            - Company Description: {company_description}
            - Company Achievements: {company_achievements}

            ### INSTRUCTION:
            You are {sender_name}, {sender_title} at {company_name}. 
            Write a cold email to the client regarding the job mentioned above describing the capability of {company_name} 
            in fulfilling their needs.

            Key points to include:
            1. A personalized opening that references specific aspects of their job posting
            2. How {company_name}'s expertise aligns with their requirements
            3. Brief mention of relevant experience and achievements
            4. If relevant portfolio links are provided, incorporate them naturally: {link_list}
            5. A clear call to action

            Tone: {tone_instruction}
            Signature: {signature_instruction}

            Remember you are {sender_name} from {company_name}. Make the email personal, engaging, and focused on the client's needs.
            Do not provide a preamble, start directly with the email content.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links,
            "sender_name": self.config["sender_name"],
            "sender_title": self.config["sender_title"],
            "company_name": self.config["company_name"],
            "company_type": self.config["company_type"],
            "company_description": self.config["company_description"],
            "company_achievements": self.config["company_achievements"],
            "tone_instruction": tone_instructions,
            "signature_instruction": signature_instructions
        })
        return res.content

    def update_config(self, **kwargs):
        """Update configuration with new values"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        self.save_user_config(self.config)


if __name__ == "__main__":
    # Example of how to use with custom configuration
    custom_config = {
        "sender_name": "John Doe",
        "sender_title": "Senior Business Development Manager",
        "company_name": "TechInnovate Solutions",
        "company_type": "Digital Transformation & AI Consulting",
        "company_description": "We specialize in helping businesses leverage cutting-edge AI and automation technologies to transform their operations.",
        "company_achievements": "We've successfully delivered 200+ projects, helping Fortune 500 companies increase efficiency by 40% and reduce operational costs by 30%.",
        "email_tone": "professional",
        "signature_style": "detailed"
    }

    chain = Chain(custom_config)
    print("Configuration loaded successfully!")