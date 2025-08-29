using Microsoft.AspNetCore.Mvc;  // ← CORRECT namespace
using MovieNest.Models;
using System.Collections.Generic;

namespace MovieNest.Controllers
{
    public class MovieController : Controller
    {
        public IActionResult Index() 
        {
            var movies = new List<Movie>
            {
                new Movie { Id = 1, Title = "Inception", Genre = "Sci-Fi", Description = "A mind-bending thriller" },
                new Movie { Id = 2, Title = "Interstellar", Genre = "Sci-Fi", Description = "Space adventure" }
            };
            return View(movies);
        }

        public IActionResult Details(int id) 
        {
            var movie = new Movie { Id = id, Title = "Inception", Genre = "Sci-Fi", Description = "A mind-bending thriller" };
            return View(movie);
        }
    }
}