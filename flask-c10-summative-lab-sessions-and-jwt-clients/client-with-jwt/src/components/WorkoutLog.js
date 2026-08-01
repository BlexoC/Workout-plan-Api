import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { Box, Button, Error, FormField, Input, Label, Textarea } from "../styles";

function WorkoutLog() {
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/workout_logs", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((r) => {
        if (!r.ok) {
          return r.json().then((err) => {
            throw new Error(err.error || err.msg || "Failed to load workout logs");
          });
        }
        return r.json();
      })
      .then((data) => {
        setLogs(data.workout_logs || []);
        setIsLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setIsLoading(false);
      });
  }, []);

  function handleCreate(newLog) {
    setLogs((prevLogs) => [newLog, ...prevLogs]);
  }

  function handleDelete(id) {
    fetch(`/workout_logs/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    }).then((r) => {
      if (r.ok) {
        setLogs((prevLogs) => prevLogs.filter((log) => log.id !== id));
      }
    });
  }

  return (
    <Wrapper>
      <WorkoutLogForm onCreate={handleCreate} setError={setError} />
      {error && <Error>{error}</Error>}
      {isLoading ? (
        <p>Loading workout logs...</p>
      ) : logs.length === 0 ? (
        <p>No workout logs yet — add one above to get started.</p>
      ) : (
        <List>
          {logs.map((log) => (
            <WorkoutLogCard key={log.id} log={log} onDelete={handleDelete} />
          ))}
        </List>
      )}
    </Wrapper>
  );
}

function WorkoutLogForm({ onCreate, setError }) {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("");
  const [durationMinutes, setDurationMinutes] = useState("");
  const [date, setDate] = useState("");
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    fetch("/workout_logs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        title,
        category,
        duration_minutes: durationMinutes ? Number(durationMinutes) : null,
        date: date || null,
        notes,
      }),
    }).then((r) => {
      setIsSubmitting(false);
      if (r.ok) {
        r.json().then((newLog) => {
          onCreate(newLog);
          setTitle("");
          setCategory("");
          setDurationMinutes("");
          setDate("");
          setNotes("");
        });
      } else {
        r.json().then((err) => setError(err.error));
      }
    });
  }

  return (
    <FormBox as="form" onSubmit={handleSubmit}>
      <FormField>
        <Label htmlFor="title">Title</Label>
        <Input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </FormField>
      <FormField>
        <Label htmlFor="category">Category</Label>
        <Input
          type="text"
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
      </FormField>
      <FormField>
        <Label htmlFor="duration_minutes">Duration (minutes)</Label>
        <Input
          type="number"
          id="duration_minutes"
          min="1"
          value={durationMinutes}
          onChange={(e) => setDurationMinutes(e.target.value)}
        />
      </FormField>
      <FormField>
        <Label htmlFor="date">Date</Label>
        <Input
          type="date"
          id="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </FormField>
      <FormField>
        <Label htmlFor="notes">Notes</Label>
        <Textarea
          id="notes"
          rows="3"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </FormField>
      <FormField>
        <Button variant="fill" color="primary" type="submit">
          {isSubmitting ? "Saving..." : "Add Workout Log"}
        </Button>
      </FormField>
    </FormBox>
  );
}

function WorkoutLogCard({ log, onDelete }) {
  return (
    <LogBox>
      <LogHeader>
        <h3>{log.title}</h3>
        <Button variant="outline" onClick={() => onDelete(log.id)}>
          Delete
        </Button>
      </LogHeader>
      <p>
        {log.category} &middot; {log.duration_minutes} min &middot; {log.date}
      </p>
      {log.notes && <p>{log.notes}</p>}
    </LogBox>
  );
}

const Wrapper = styled.section`
  max-width: 600px;
  margin: 24px auto;
  padding: 0 16px;
`;

const FormBox = styled(Box)`
  margin-bottom: 24px;
`;

const List = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const LogBox = styled(Box).attrs({ as: "li" })`
  border: 1px solid #dbdbdb;
`;

const LogHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    margin: 0;
  }
`;

export default WorkoutLog;