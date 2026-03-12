from agent.adk_client import ask_agent


if __name__ == "__main__":
    print("NHRIS Google ADK Agent (client)")
    while True:
        q = input("Ask: ")
        if not q:
            break
        try:
            print(ask_agent(q) or "No response from agent.")
        except Exception as e:
            print(f"ADK error: {e}")
