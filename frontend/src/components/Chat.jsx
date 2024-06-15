import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import NewMessage from "./NewMessage";

const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

function Chats() {
  const { chatID } = useParams();
  return (
    <div className="chats-page">
      {chatID ? <MessageCardQueryContainer chatID={chatID} /> : <h2>Select a Chat</h2>}
    </div>
  );
}

// -------- Messages ----------
function MessageCardQueryContainer({ chatID }) {
  const { data } = useQuery({
    queryKey: ["chats", chatID, "messages"],
    queryFn: () => (
      fetch(`${baseUrl}/chats/${chatID}/messages`)
        .then((response) => response.json())
    ),
  });

  if (data) {
    return <MessageListContainer messages={data.messages} />
  }

  return <h2>loading...</h2>
}

function MessageListItem({ message }) {
  const date = new Date(message.created_at);
  const formattedDate = date.toDateString();
  const formattedTime = date.toLocaleTimeString();
  return (
    <div key={message.id} name="message-list-item" className="flex flex-col border border-cyan-600 rounded w-[1200px] m-7 p-3">
      <div name="message-info" className="flex flex-row justify-between">
        <div name="message-list-item-userID" className="text-xs">
          {message.user.username}
        </div>
        <div name="message-list-item-date" className="text-xs">
          {formattedDate} - {formattedTime}
        </div>
      </div>
      <div name="message-list-text" className="text-s">
        {message.text}
      </div>
    </div>
  )
}

function MessageList({ messages }) {
  return (
    <div className="overflow-y-auto max-h-[480px]">
      {messages.map((message) => (
        <MessageListItem key={message.id} message={message} />
      ))}
    </div>
  )
}

function MessageListContainer({messages}) {
  return(
    <div className="flex flex-col">
      <h2 className="text-2xl px-4 py-4">Messages</h2>
      <MessageList messages={messages} />
      <NewMessage />
    </div>
  )
}

export default Chats;