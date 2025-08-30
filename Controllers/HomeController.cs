using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using MovieNest.Models;

namespace MovieNest.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public ActionResult Index()
    {
        var movies = new List<Movie>
        {
            new Movie{Id=1, Title="Inception", Genre="Sci-Fi", Description="A mind-bending thriller", VideoUrl="https://www.youtube.com/embed/YoHD9XEInc0"},
            new Movie{Id=2, Title="The Matrix", Genre="Sci-Fi", Description="Reality is a simulation", VideoUrl="https://www.youtube.com/embed/vKQi3bBA1y8"},
            new Movie{Id=3, Title="Spirited Away", Genre="Animation", Description="A young girl's adventure", VideoUrl=string.Empty}
        };

        ViewBag.Message = "Welcome to MovieNest 🎬";
        return View(movies);
    }
    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
    
    public IActionResult Details(int? id)
{
    if (id == null || id <= 0)
    {
        return NotFound();
    }

    var movie = new Movie
    {
        Id = id.Value,
        Title = "Inception",
        Genre = "Sci-Fi",
        Description = "A mind-bending thriller",
        VideoUrl = string.Empty 
    };

    return View(movie);
}
}
