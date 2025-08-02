export async function generateStory(image: File, genre: string, prompt: string): Promise<string> {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("genre", genre);
  formData.append("prompt", prompt);

  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  return data.story;
}