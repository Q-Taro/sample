import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatOpenAI

# Password for access
PASSWORD = "57$%2439Mhndsf%#90sdfB"


def create_agent_chain():
    chat = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],
        openai_api_base=os.getenv("OPENAI_API_BASE"),  # For Azure OpenAI API
        temperature=os.environ["OPENAI_API_TEMPERATURE"],
        streaming=True,
    )
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    tools = load_tools(["ddg-search", "wikipedia"])
    return initialize_agent(
        tools,
        chat,
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )

# Ask for password
def password_protect():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Enter Password", type="password")
        if password == PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Incorrect password")
            st.stop()

# Call the password protection function
password_protect()

# Once authenticated, the rest of the app runs
st.title("langchain-streamlit-app")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")

if "agent_chain" not in st.session_state:
    st.session_state.agent_chain = create_agent_chain()
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.agent_chain.run(prompt, callbacks=[callback])
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})





#with st.chat_message("assistant")
#    chat = ChatOpenAI(model_name=os.environ["OPENAI_API_MODEL"]),
#    temperature=os.environ["OPENAI_API_TEMPERATURE"])
#messages = [HumanMessage(content=prompt)]

# end of script