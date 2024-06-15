import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth, useApi } from "../hooks";
import Button from "./Button";

function Input(props) {
  return (
    <div className="flex flex-col py-2">
      <input
        {...props}
        className="border rounded w-[1100px] bg-transparent px-2 py-1"
      />
    </div>
  )
}

function NewMessageForm({ chatID }) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { token } = useAuth();
  const api = useApi();

  const [text, setText] = useState("");

  const mutation = useMutation({
    mutationFn: () => (
      api.post(
        `/chats/${chatID}/messages`,
        {
          text
        },
        {
            headers: {
              Authorization: `Bearer ${token}`
            }
        }
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["chats"],
      });
      navigate(`/chats/${chatID}`);
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <form onSubmit={onSubmit} className="flex flex-row items-center justify-between w-[1245px] px-4 py-4">
      <Input
        type="text"
        placeholder="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <Button type="submit">send</Button>
    </form>
  )
}

function NewMessage() {
    const { chatID } = useParams();
    return (chatID ? <NewMessageForm chatID={chatID} /> : null)
}

export default NewMessage;