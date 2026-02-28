import Editor from "@/components/Editor";
import { auth0 } from "@/lib/auth0";

const EditorPage = async () => {
  const session = await auth0.getSession();

  if (!session) {
    return (
      <div>
        <h1>You must be logged in to access the editor</h1>
      </div>
    );
  }
  return (
    <div className="min-h-[calc(100vh-5rem)]">
      <Editor />
    </div>
  );
};

export default EditorPage;
