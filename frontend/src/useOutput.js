import { useCallback, useEffect, useState } from "react";
import { generate, getOutput } from "./api";

export function useOutput(docId, kind) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [version, setVersion] = useState(0);

  useEffect(() => {
    setData(null);
    setError("");
    if (!docId) return;
    getOutput(docId, kind)
      .then((r) => {
        setData(r.data);
        setVersion((v) => v + 1);
      })
      .catch(() => {});
  }, [docId, kind]);

  const run = useCallback(
    async (count) => {
      setLoading(true);
      setError("");
      try {
        const r = await generate(docId, kind, count);
        setData(r.data);
        setVersion((v) => v + 1);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    },
    [docId, kind]
  );

  return { data, loading, error, run, version };
}
