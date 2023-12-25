import gradio as gr

from helper import *

with gr.Blocks() as demo:
    session_id = gr.State(create_session_id)
    gr.Markdown('''<h1 style="text-align: center;">Vector index document query </h1>''')

    collection = gr.Textbox(
        value='collection1', label='Data collection name', info='No special characters'
    )

    # adding data
    gr.Markdown(
        '''<h2 style="text-align: center;"> For each data collection, ADD >1 CONTEXT BEFORE QUERY </h2>''')
    # output for query
    chatbot = gr.Chatbot(label='related document')
    chatbot2 = gr.Chatbot(label='related document + GPT')
    msg = gr.Textbox()
    submit_btn = gr.Button('submit')
    submit_btn.click(fn=respond, inputs=[session_id, collection, msg, chatbot, chatbot2],
                     outputs=[msg, chatbot, chatbot2])
    # msg.submit(respond, [session_id, msg, chatbot], [msg,chatbot])
    # clear = gr.ClearButton([msg, chatbot])

    source_url = gr.Textbox(label='Context URL')
    source_btn = gr.Button('Add data from URL')
    source_btn.click(fn=add_url, inputs=[session_id, collection, source_url], outputs=[source_url])

    source_file = gr.File(
        type='filepath', label='Accept text file & .docx')
    source_btn = gr.Button('Add data from File')
    source_btn.click(fn=add_file, inputs=[session_id, collection, source_file], outputs=[source_file])

if __name__ == "__main__":
    demo.queue().launch(server_name='0.0.0.0', share=True)
