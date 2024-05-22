import streamlit as st
import pandas as pd
from textblob import TextBlob

# Define a function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def main():
    st.markdown(
        """
        <style>
        body {
            background-color: #f6f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.image("nsf_icorps_survey.png", caption="Survey: Understanding Customer Needs, Behaviors, Emotions & Decisions", use_column_width=True)

    questions = [
        {"id": "Q1", "category": "Behavior", "question": "How often do you currently use data-driven strategies to influence customer behavior in your marketing efforts?"},
        {"id": "Q2", "category": "Behavior", "question": "When implementing new marketing technologies, how often do you test their impact on customer behavior (A/B testing) or other methodologies before full integration? "},
        {"id": "Q3", "category": "Behavior", "question": "Do your marketing strategies incorporate data analytics utilizing AI?"},
        {"id": "Q4", "category": "Behavior", "question": "Do you track the effectiveness of different marketing content relative to customer meta-data?"},
        {"id": "Q5", "category": "Behavior", "question": "How frequently do you update your marketing strategies based on customer behavioral data insights?"},
        {"id": "Q6", "category": "Behavior", "question": "If more descriptive data derived directly from your marketing content with a potentially higher targeted customer demographic conversion rate was available would you buy it?"},
        {"id": "Q7", "category": "Emotion", "question": "Is it important to you to understand customer emotions relative to your marketing strategy?"},
        {"id": "Q8", "category": "Emotion", "question": "How often do you use any tools or technologies to gauge emotional reactions to your advertisements?"},
        {"id": "Q9", "category": "Emotion", "question": "How frequently do you modify marketing materials to better align with customer emotions?"},
        {"id": "Q10", "category": "Emotion", "question": "Does your content strategy prioritize eliciting emotional responses relative to influencing potential behavior?"},
        {"id": "Q11", "category": "Emotion", "question": "Do you believe utilizing emotional data is effective in enhancing customer engagement?"},
        {"id": "Q12", "category": "Emotion", "question": "Do you feel that your current tools are insufficient for the depth of data analysis you aspire to achieve?"},
        {"id": "Q13", "category": "Decision", "question": "Does data influence your decisions on creating new marketing campaigns?"},
        {"id": "Q14", "category": "Decision", "question": "How often have you changed a marketing decision based on insights from customer data analysis?"},
        {"id": "Q15", "category": "Decision", "question": "Would you adopt a new technology, if it demonstrated a clear advantage in influencing customer decisions?"},
        {"id": "Q16", "category": "Decision", "question": "Do you believe that the right data and tailored content can significantly alter marketing outcomes?"},
        {"id": "Q17", "category": "Decision", "question": "Does your organization prioritize learning more about using advanced data methodologies and Artificial Intelligence to predict and shape customer purchase decisions?"},
        {"id": "Q18", "category": "Decision", "question": "Is technological innovation a priority in your marketing department?"},
        {"id": "Q19", "category": "Decision", "question": "Would you invest in technology that predicts customer behavior with higher accuracy, even if it cost more?"},
        {"id": "Q20", "category": "Decision", "question": "How often do you seek out new technologies to improve data accuracy in your marketing efforts?"},
        {"id": "Q21", "category": "Decision", "question": "Would you find a tool that automates the alignment of marketing content with emotional and behavioral data useful?"}
    ]

    responses = {}
    
    st.subheader("Instructions")
    st.write("Informed Consent - The data collected in this survey is completely anonymous. There isn't any personally identifiable information that will be collected and the information that you choose to provide cannot be traced back to you. Your participation is voluntary and you may choose not to participate or end your participation at any time without penalty. There isn't any compensation provided for participating in the survey. I have read, understand and consent to all of the terms provided and certify that I am 18 years old or older.")

    with st.form(key='customer_needs_survey', clear_on_submit=True, border=True):
        consent = st.checkbox('By clicking this checkbox and/or Submit Response button, I indicate my willingness to voluntarily take part in this survey.', value=False, key='consent')
        
        role = st.selectbox(
            'What is Your Role in the Organization',
            ("Director", "CEO", "CIO", "CTO", "CFO", "Legal", "Marketing Manager", "Technology", "Sales", "Public Relations", "Data Analyst", "Social Media", "SEO", "Brand Strategist", "Futurist", "R&D", "Product Development", "Other", "Rather Not Say"))
            
        industry = st.text_input('Industry:', value="", max_chars=25)    
        
        company_size = st.selectbox(
            'What is the Size of Your Organization?',
            ("Micro: 1 to 9 employees", "Small: 10 to 49 employees", "Medium: 50 to 249 employees", "Large: 250 or more employees", ))
            
        st.info("Questions & Answers: |-1 Never | 0 Sometimes | 1 Always|")
        
        for q in questions:
            response = st.slider(q["question"], -1.0, 1.0, 0.0, 0.1, key=q["id"])
            responses[q["id"]] = response
        
        text = st.text_area('Write a few sentences that explains how you feel about utilizing AI and human behavioral, emotion and decision data to craft and align marketing content to achieve higher conversion rates and sales.')
        
        text2 = st.text_area('Is/are there any question(s) that you would like to answer that was/were not asked?')
        
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            sentiment_score = analyze_sentiment(text)
            
            
            # Create DataFrame with one row for the current responses
            response_data = {
                "Consent": consent,
                "Role": role,
                "Industry": industry,
                "Company_Size": company_size,
                "Sentiment": "%.2f" % sentiment_score,
                "Addl_Quest": text2,
                **responses
            }
            df = pd.DataFrame([response_data])
                                 
            st.success("Responses submitted successfully!")
            st.balloons()
            average = "%.2f" % ((df.iloc[:, 6:].sum(axis=1).values[0] + (sentiment_score * 3)) / 24)
            df.insert(27, "Overall", average)
            st.subheader(f"Your Overall Score: {average}")
            # Save DataFrame to CSV file, appending new responses as rows
            df.to_csv("survey_responses.csv", mode='a', header=not pd.io.common.file_exists("survey_responses.csv"), index=False)
            st.image("results.png", use_column_width=True)
            st.write("This survey methodology leverages both structured responses and AI-driven sentiment analysis to provide a comprehensive evaluation of your organization's potential needs as it relates to behavioral, emotional, and decision data products. The structured questions are designed to capture specific behaviors, emotions, and decision-making processes within your organization, assessing the direct applicability and potential benefits of our novel data architecture. Your responses will help us better understand the market's readiness to adopt such technology, the perceived value of data-driven insights in marketing strategies and facilitate overall customer discovery. The sentiment analysis component enhances this by quantifying the emotional tone of your responses, offering additional depth to our understanding. Together, these methods yield a holistic Sentiment Score and an Overall Score, which reflect both the qualitative and quantitative feedback on your organization's inclination towards our future product offering.")
            st.write("The Overall Score, calculated by integrating survey responses with the weighted sentiment analysis, serves as a metric of potential need and receptiveness. A score closer to +1 indicates a strong alignment and perceived necessity for our products, suggesting that your type of organization might greatly benefit from their implementation. Conversely, a score closer to -1 highlights areas where our solutions may not currently align with your type of organization's practices or immediate needs. By submitting your survey responses, you are contributing valuable insights that enable us to tailor our business model more effectively. The data collected will also be crucial in guiding the ongoing development and refinement of our technology, ensuring that it remains at the cutting edge of data-driven solutions. Thank you for your participation.")
            
    st.write("If you would like to receive a copy of the final summary of results when the survey closes, or have any questions or concerns with respect to the survey please contact Marcus Rodriguez, i*. marcuscrodriguez@outlook.com / www.marcusc.com.")

if __name__ == "__main__":
    main()

