import commons


q1 = commons.Queue(10)

print(f"The array of the queue before: {q1.array}")
print(f"The front of queue before:{q1.peek()}")
for i in range(11):
    try:
        q1.enqueue(f"Hello World {i}")
    except Exception:
        print("couldn't add to queue")

print(f"The array of the queue while queued: {q1.array}")
print(f"The front of queue while queued :{q1.peek()}")

print(q1.dequeue())
print(q1.dequeue())

print(f"The front of queue after :{q1.peek()}")
print(f"The array of the queue after: {q1.array}")