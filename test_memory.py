from main.memory.memory_manager import MemoryManager

m = MemoryManager()

print(m.get_all_memories())
print(m.get_memory("user", "name"))