import VueGtag from "vue-gtag";

export default ({ app, router }) => {
  if (process.env.DEV) return;
  app.use(
    VueGtag,
    {
      config: { id: "G-77N5QB2V4D" },
    },
    router
  );
};
