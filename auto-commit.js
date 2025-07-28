const { exec } = require("child_process");
const chokidar = require("chokidar");

const watcher = chokidar.watch(".", {
  ignored: /(^|[\/\\])\../, // abaikan file dot seperti .git, .vscode
  persistent: true
});

watcher.on("change", path => {
  console.log(`File ${path} changed. Committing...`);
  exec(
    'git add . && git commit -m "Auto update" && git push origin main',
    (err, stdout, stderr) => {
      if (err) {
        console.error("Gagal commit:", stderr);
      } else {
        console.log("Berhasil push:\n", stdout);
      }
    }
  );
});
