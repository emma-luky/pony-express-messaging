import Chat from "./Chat";
import LeftNav from "./LeftNav";

function Chats() {
  return (
    <div className="flex flex-row h-main">
      <div className="w-60">
        <LeftNav />
      </div>
      <div className="mx-auto">
        <Chat />
      </div>
    </div>
  );
}

export default Chats;