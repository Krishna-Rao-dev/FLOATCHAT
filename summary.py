from sql_table import returnRows,response
from gemini_sql import generateQuery

arr = [
    f"""
    {returnRows(response)}
"""]
prompt = [
    """
    
    YOU ARE A DATA ANALYZER FOR THE SQL QUERY RESPONSE THAT YOU GET AS A QUERY\n
    THE DATA PROVIDED IS OCEAN ARGO DATA, SO BE CONTEXTUAL AROUND IT\n
    BE REALISTIC DONT HALLUCINATE OR CREATE NEW DATA, STICK TO WHAT IS PROVIDED\n
    ENSURE QUALITY OUTPUTS\n
    ALTHOUGH YOU ARE A DATA ANAYLZER FOR SQL, DONT INCLUDE WORDS RELATED TO SQL like:\n
    --Example 1---
    INCORRECT: The provided SQL query result, a data tuple `(10.523094611450471, 971.2524209537997)` rather say:\n
    CORRECT: The provided resultant is, a data tuple `(10.523094611450471, 971.2524209537997)`\n
    --Example 2--- 
    INCORRECT: Based on the characteristic structure and typical ranges of Ocean Argo data parameters, this specific data point from the SQL query most probably represents an **ocean temperature of approximately 10.52 degrees Celsius, observed at a depth/pressure of roughly 971.25 meters** within an Argo float's vertical measurement profile.\n
    CORRECT: Based on the characteristic structure and typical ranges of Ocean Argo data parameters, this specific data point most probably represents an **ocean temperature of approximately 10.52 degrees Celsius, observed at a depth/pressure of roughly 971.25 meters** within an Argo float's vertical measurement profile.\n
    """
]

prompt_summarizer = [
    """

    GENERAL INFO : YOU ARE DEALING WITH OCEAN ARGO DATA SQL SUMMARIZED\n
    ROLE:YOU ARE A SQL DATA ANALYSIS TO SUMMARIZER & YOU ARE ACTUALLY AN API ENDPOINT RESPONSE FOR A CHATTING APPLICATION, SO IN THAT CONTEXT SUMMARIZE, DON'T BE TOO MUCH THEORTICAL IN YOUR ANSWERS, BUT THAT DOESNT MEAN THAT YOU ARE ESSENTIAL NOT SUMMARIZING THE DATA ANALYSIS\n
    SUMMARIZE VERY ACCURATELY, BUT DON'T LOOSE THE ESSENCE MEANING, THE QUERY THAT YOU GET IN YOUR INPUT, WOULD BE A BIT LARGE, SO WHILE SUMMARIZING JUST DONT SHORTEN TO SOMETHING VERY SHORT,\n
    RATHER, KEEP THE LANGUAGE, KEEP THE WORDINGS, KEEP THE TERMINOLOGIES, KEEP THE REPORT ANALYSIS IN THE MAIN PICTURE.\n
    ALSO YOU MAY RECEIVE SOME TERMS LIKE "DATA ANALYSIS" or "SQL QUERY" - YOUR MAIN JOB IS TO TURN THAT OVER SUCH THAT, USER WHO SEE YOUR RESPONSE, MUST RELATED IT TWO HUNDRED PERCENT WITH THE DATA\n
    MAKE IT ALL AROUND THE OCEAN ARGO DATA TERMINLOGIES, WORDINGS, PARAMETERS, AND STATISTICAL ANALYSIS\n
    VERY IMP- DO NOT LOOSE UPON THE ESSENCE OF STATISTICAL ANAYLSIS SUMMARIZED TEXT CONTEXT\n
    BUT, ALSO ENSURE THAT YOU ARE NOT HALLUCINATING UPON ANY DATA
    """
]
analyzed = generateQuery(prompt,arr[0])

print(generateQuery(prompt_summarizer,analyzed))