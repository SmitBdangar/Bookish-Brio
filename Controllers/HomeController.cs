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
        ViewBag.Message = "Welcome to MovieNest 🎬";
        return View();
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
