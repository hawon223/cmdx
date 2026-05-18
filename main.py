import typer

app = typer.Typer()

@app.command()
def ask(query: str):
    print(f"입력: {query}")
    
if __name__=="__main__":
    app()
