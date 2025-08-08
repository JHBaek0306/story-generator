export async function generateStory(image: File, genre: string, prompt: string): Promise<any> {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("genre", genre);
  formData.append("user_input", prompt);

  const res = await fetch("http://localhost:8000/generate_story/", {
    method: "POST",
    body: formData,
  });
  const data = await res.json();
  return data;
}