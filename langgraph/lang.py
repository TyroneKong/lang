from typing import TypedDict, Literal, Union
from langgraph.graph import START, END


class Agent(TypedDict):
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    operation_1: str
    operation_2: str
    final_1: Union[int, float]
    final_2: Union[int, float]


def plus(state: Agent) -> Agent:
    state['final_1'] = state['number_1'] + state['number_2']
    return state


def minus(state: Agent) -> Agent:
    state['final_1'] = state['number_1'] - state['number_2']
    return state


def multiply(state: Agent) -> Agent:
    state['final_2'] = state['number_3'] * state['number_4']
    return state


def divide(state: Agent) -> Agent:
    state['final_2'] = state['number_3'] / state['number_4']
    return state


def conditional(state: Agent) -> Literal["minus", "plus"]:
    if state['operation_1'] == '+':
        return "plus"
    elif state['operation_1'] == '-':
        return "minus"


def conditional2(state: Agent) -> Literal[ "multiply", "divide"]:
    if state['operation_2'] == '*':
        return "multiply"
    elif state['operation_2'] == '/':
        return "divide"



graph = StateGraph(Agent)

graph.add_node('conditional_1', lambda state: state)
graph.add_node('add_node_1', plus)
graph.add_node('subtract_node_1', minus)

graph.add_node('conditional_2', lambda state: state)
graph.add_node('multiply_node_2', multiply)
graph.add_node('divide_node_2', divide)

graph.add_edge(START, 'conditional_1')

graph.add_conditional_edges('conditional_1', conditional, {
    'minus': 'subtract_node_1',
    'plus': 'add_node_1',

})
graph.add_edge('add_node_1', 'conditional_2')
graph.add_edge('subtract_node_1', 'conditional_2')
graph.add_conditional_edges('conditional_2', conditional2, {

    'multiply': 'multiply_node_2',
    'divide': 'divide_node_2',
})




compiled_graph = graph.compile()

# Visualize your graph
from IPython.display import Image, display

png = compiled_graph.get_graph().draw_mermaid_png()
display(Image(png))

result = compiled_graph.invoke({'number_1': 10, 'number_2': 3, 'operation_1': '-', 'number_3':10, 'number_4':5,'operation_2':'/'})
result['final_1']
result['final_2']

