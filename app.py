import streamlit as st 
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from model.rag import Rag

@st.cache_resource()
def load_rag():
    return Rag()
    

def main() :
    chain  = load_rag()

    st.title('dakshampoo-shop.nl chatbot')
    st.write('This is a chatbot that can help you with questions about dakshampoo-shop.nl')

    if 'chat_history' not in st.session_state.keys():
        st.session_state['chat_history']=[]
    
    chat_history = st.session_state['chat_history']
            

    WELCOME_MESSAGE = "Welcome!"
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role":"assistant","content":f"{WELCOME_MESSAGE}"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):  # Use dot notation here
            st.markdown(message["content"])  # And here

    if question := st.chat_input("Your message..."):
        new_message = {"role":"user","content":f"{question}"}
        st.session_state.messages.append(new_message)
        
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())
            message_placeholder = st.empty()
            full_response = ""
            # HERE WE WILL CALL THE MODEL
            response = chain.run(question, st_callback=st_callback)
            answer = response['answer']
            st.write(answer)
            # HERE WE STORE MEMORY OF THE CONVERSATION
            # st.session_state.chat_history.append(human_question)
            # st.session_state.chat_history.append(ai_response)

            # HERE WE SHOW RESPONSE 
            st.session_state.messages.append({"role":"assistant","content":answer})



if __name__ =="__main__":
    main() 