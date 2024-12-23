import {AuthenticationError, ValidationError} from "../helpers/errors";
import express from "express";
import {isAuthenticatedMiddleware} from "./auth";
import {getTasks, createTask} from "../lib/tasks";



export const tasksRouter = express.Router();

// Get current user
tasksRouter.get("/", isAuthenticatedMiddleware, async (req, res, next) => {
  if (!req.user) return next(new AuthenticationError());
  const tasks = await getTasks(req.user.id);

  return res.send(tasks);
});

tasksRouter.post("/", isAuthenticatedMiddleware, async (req, res, next) => {
    if (!req.user) return next(new AuthenticationError());
    const { title, content } = req.body;

    if (!title || !content) {
        return next(new ValidationError("Title and content are required"));
    }

    const task = await createTask(req.user.id, title, content);

    return res.status(201).send(task);
    });
