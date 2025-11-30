const supabase = require("./db");

async function test() {
  const { data, error } = await supabase.from("users").select("*");
  if (error) console.log("DB ERROR:", error);
  else console.log("Users in DB:", data);
}

test();
