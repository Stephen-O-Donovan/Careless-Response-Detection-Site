import streamlit as st

st.set_page_config(
    page_title="Meta",
    page_icon="",
)

st.write("How this site was built")

with st.expander("A (growing) list of tech used"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
    st.header('AWS')
    st.subheader('Fargate')
    st.subheader('ECR')
    st.subheader('S3')
    st.subheader('SAM')
    st.subheader('Lambda')
    st.subheader('Lambda Layers')
    st.subheader('API Gateway')
    st.subheader('Secret Manager')
    st.subheader('AWS CLI')
    st.header('Local Dev')
    st.subheader('Git')
    st.subheader('Docker')
    st.subheader('Streamlit')