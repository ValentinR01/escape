import { logger } from "../helpers/logger";
import { prisma } from "../helpers/prisma";
import type { Task } from "@prisma/client";

export const getTasks = async (userId : string): Promise<Task[]> => {
  try {
    const tasks = await prisma.task.findMany({
      where: {
          userId: userId,
      }
    });
    return tasks;
  } catch (error) {
    logger.error(`Error fetching tasks: ${error}`);
    throw error;
  }
};

export const createTask = async (userId: string, title: string, content: string): Promise<Task> => {
    const task = await prisma.task.create({
      data: {
        title,
        content,
        status: "PENDING",
        userId,
      },
    });
    return task;
};