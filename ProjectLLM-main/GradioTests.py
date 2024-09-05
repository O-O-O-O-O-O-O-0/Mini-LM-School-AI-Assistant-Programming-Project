import gradio as gr
import EmbeddingsRunQ

def runQ(inputQ):
    output, scores, links = EmbeddingsRunQ.run_everything(inputQ)
    return output, scores, links
     

demo = gr.Interface(fn=runQ, inputs="text", outputs="text")
    
if __name__ == "__main__":
    demo.launch(show_api=False, share=True)
