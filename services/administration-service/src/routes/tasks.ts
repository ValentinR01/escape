import { AuthenticationError} from "../helpers/errors";
import express from "express";
import {isAuthenticatedMiddleware} from "./auth";
import {getTasks} from "../lib/tasks";


export const tasksRouter = express.Router();

// Get current user
tasksRouter.get("/", isAuthenticatedMiddleware, async (req, res, next) => {
  if (!req.user) return next(new AuthenticationError());
  const tasks = await getTasks(req.user.id);

  return res.send(tasks);
});

