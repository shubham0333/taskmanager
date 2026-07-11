import React, { useEffect, useState } from "react";
import { Check, Pencil, Trash, Save } from "lucide-react";
import { ENDPOINTS, instance } from "./api";
import { toast } from "react-toastify";

const Task = () => {
  const [tasks, setTasks] = useState([]);
  const [editable, setEditable] = useState(null);
  const [inputTask, setInputTask] = useState("");

  // Edit task title
  const editTask = (e, id) => {
    setTasks((items) =>
      items.map((item) =>
        item.id === id ? { ...item, title: e.target.value } : item
      )
    );
  };

  // Save edited task
  const saveTask = async (id) => {
    const task = tasks.find((task) => task.id === id);

    if (!task) return;

    try {
      await instance.put(ENDPOINTS.UPDATE_TASK(id), {
        title: task.title,
        description: task.description,
        completed: task.completed,
      });

      toast.success("Task updated successfully");
      setEditable(null);
      getAllTasks();
    } catch (err) {
      console.log(err);
    }
  };

  // Complete task
  const completeTask = async (id) => {
    const task = tasks.find((task) => task.id === id);

    if (!task) return;

    try {
      await instance.put(ENDPOINTS.UPDATE_TASK(id), {
        title: task.title,
        description: task.description,
        completed: !task.completed,
      });

      toast.success("Task updated successfully");
      getAllTasks();
    } catch (err) {
      console.log(err);
    }
  };

  // Add task
  const addTask = async () => {
    if (inputTask.trim() === "") return;

    try {
      await instance.post(ENDPOINTS.CREATE_TASK(), {
        title: inputTask,
        completed: false,
      });

      toast.success("Task created successfully");
      setInputTask("");
      getAllTasks();
    } catch (err) {
      console.log(err);
    }
  };

  // Fetch tasks
  const getAllTasks = async () => {
    try {
      const res = await instance.get(ENDPOINTS.GET_TASK());

      console.log(res.data);

      if (Array.isArray(res.data)) {
        setTasks(res.data);
      } else {
        setTasks([]);
      }
    } catch (err) {
      console.log(err);
      setTasks([]);
    }
  };

  // Delete task
  const deleteTask = async (id) => {
    try {
      await instance.delete(ENDPOINTS.DELETE_TASK(id));

      toast.success("Task deleted successfully");
      getAllTasks();
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    getAllTasks();
  }, []);

  return (
    <>
      <div className="container">
        <div className="input-box">
          <input
            type="text"
            value={inputTask}
            onChange={(e) => setInputTask(e.target.value)}
          />
          <span className="add" onClick={addTask}>
            Add
          </span>
        </div>

        <div className="task-container">
          {tasks.map((item) => (
            <div
              key={item.id}
              className="task-items"
              style={{
                backgroundColor: item.completed ? "#98FF98" : "white",
              }}
            >
              <div className="task-title">
                <div>
                  <label className="title">Title : </label>

                  <input
                    type="text"
                    value={item.title}
                    disabled={editable !== item.id}
                    onChange={(e) => editTask(e, item.id)}
                  />
                </div>

                <Check
                  size={20}
                  style={{ cursor: "pointer" }}
                  onClick={() => completeTask(item.id)}
                />
              </div>

              <div className="icon-group">
                {editable !== item.id ? (
                  <Pencil
                    size={20}
                    style={{ cursor: "pointer" }}
                    onClick={() => setEditable(item.id)}
                  />
                ) : (
                  <Save
                    size={20}
                    style={{ cursor: "pointer" }}
                    onClick={() => saveTask(item.id)}
                  />
                )}

                <Trash
                  size={20}
                  style={{ cursor: "pointer" }}
                  onClick={() => deleteTask(item.id)}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Task;