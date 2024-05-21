import os
import asyncio
from secretkey import googleapi_key
os.environ["GOOGLE_API_KEY"]=googleapi_key

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import SequentialChain,LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
op_parser=StrOutputParser()

async def generate_restaurant_name_and_items(cuisine):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0.8)
        res={}
        prompt_template_name=PromptTemplate(
            input_variables=['cuisine'],
            template="I want to open a {cuisine} food restaurant. Suggest me only one random short name so that it is unique to others"
        )
        name_chain=prompt_template_name|llm|{"name":op_parser}
        res['restaurant_name']=name_chain.invoke(cuisine)['name']

        prompt_template_items=PromptTemplate(
            input_variables=['restaurant_name'],
            template="Suggest me only 10 menu items for {restaurant_name}. Return as comma separated single list in a single line and don't number them"
        )
        menu_chain=prompt_template_items|llm|{"menu":op_parser}
        res['menu_items']=menu_chain.invoke(res['restaurant_name'])['menu']

        prompt_template_slogan=PromptTemplate(
            input_variables=['restaurant_name'],
            template="Suggest me only one slogan for restaurant {restaurant_name}"
        )
        slogan_chain=prompt_template_slogan|llm|{"slogan":op_parser}
        res['slogan']=slogan_chain.invoke(res['restaurant_name'])['slogan']  
        return res
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
